# Cross-Language Specification: HTTP Access Log Analyzer

**Target Algorithm:** Streaming Combined Log Format (CLF) Analyzer  
**Scope:** Language-agnostic behavioral contract for polyglot implementations (e.g., Python, Node.js/JavaScript, Go, Rust, Java)  
**Primary Goal:** Bit-for-bit functional equivalence across implementations while preserving $O(N)$ streaming time and $O(U + P)$ memory complexity.

---

## 1. CLI & Execution Contract

Each implementation MUST expose a command-line interface with identical argument handling and exit codes:

```text
<executable> <input_file_path>
```

| Condition | `stdout` | `stderr` | Exit Code |
| :--- | :--- | :--- | :---: |
| Valid readable file (including empty or all-malformed files) | Single JSON object | Empty | `0` |
| Missing argument or more than 1 positional argument | Empty | Diagnostic message | `1` |
| Input path does not exist, is a directory, or cannot be opened | Empty | Diagnostic message | `1` |

Implementations MUST stream the file line-by-line rather than loading the entire file into memory at once (`read()`, `fs.readFileSync`, `os.ReadFile`, etc. are disallowed for production/benchmark compliance).

---

## 2. Input Format

### 2.1 Encoding & Line Normalization
- **Character encoding:** UTF-8. Invalid byte sequences MUST NOT crash or abort processing; decoders MUST replace invalid sequences with `U+FFFD` (Unicode replacement character).
- **Line endings:** Both LF (`\n`) and CRLF (`\r\n`) MUST be supported. Strip trailing `\r` and `\n` from each line before parsing.
- **Blank lines:** Lines that are empty or contain only ASCII spaces (`' '`) and horizontal tabs (`'\t'`) after stripping `\r\n` MUST be skipped. They do NOT increment `total_requests` or `malformed_lines`.

### 2.2 Record Grammar (Combined Log Format)
Every non-blank line MUST match the following space-delimited structure (single ASCII space `' '` between top-level tokens):

```text
<client_ip> <ident> <auth_user> [<timestamp>] "<method> <path> <protocol>" <status> <bytes> "<referer>" "<user_agent>"
```

Reference regular expression (PCRE / RE2 / Python compatible):

```regex
^(\S+) (\S+) (\S+) \[(\d{2}/(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/\d{4}:\d{2}:\d{2}:\d{2} [+-]\d{4})\] "([A-Z]+) (\S+) (HTTP/\d+\.\d+)" (\d{3}) (-|\d+) "((?:[^"\\]|\\.)*)" "((?:[^"\\]|\\.)*)"$
```

### 2.3 Field Validation Rules

| Field | Rule |
| :--- | :--- |
| `client_ip` | Non-empty token without whitespace (`\S+`). Treated as an opaque string key (IPv4, IPv6, or hostname). |
| `ident`, `auth_user` | Non-empty token without whitespace (`\S+`, typically `-`). Validated structurally, not emitted. |
| `timestamp` | Must match `DD/Mon/YYYY:HH:MM:SS [+-]ZZZZ` where `Mon` is a 3-letter English month (`Jan`–`Dec`), `01 <= DD <= 31`, `00 <= HH <= 23`, `00 <= MM <= 59`, `00 <= SS <= 59`. Full Gregorian calendar validation (e.g., Feb 30) is intentionally out of scope to prevent date-library divergence across languages. |
| `method` | One or more uppercase ASCII letters (`[A-Z]+`). |
| `path` | Non-empty token without whitespace (`\S+`). Must start with `'/'` or equal `"*"` (for `OPTIONS *`). Query strings are preserved as part of `path`. |
| `protocol` | Must match `HTTP/\d+\.\d+` (e.g., `HTTP/1.0`, `HTTP/1.1`, `HTTP/2.0`). |
| `status` | 3-digit integer in the inclusive range `[100, 599]`. |
| `bytes` | Either `"-"` (normalized to `0`) or an unsigned base-10 integer in `[0, 9223372036854775807]` (`INT64_MAX`). |
| `referer`, `user_agent` | Double-quoted strings supporting escaped characters (`\"`, `\\`). Empty quotes `""` are valid. Validated structurally, not emitted. |

Any non-blank line failing any rule above MUST be rejected as malformed: increment `malformed_lines` by `1` and continue processing subsequent lines.

---

## 3. Algorithm Description

### 3.1 Single-Pass Streaming Aggregation
Initialize state:
- `total_requests = 0`
- `malformed_lines = 0`
- `total_bytes = 0` (64-bit integer)
- `status_classes = {"1xx": 0, "2xx": 0, "3xx": 0, "4xx": 0, "5xx": 0}`
- Hash maps (initially empty): `visitors[ip] -> count`, `paths[path] -> count`, `methods[method] -> count`

For each line read from the stream:
1. Strip trailing `\r\n`; if blank (`""` or only `' '`/`'\t'`), continue.
2. Parse and validate against Section 2.2 and 2.3. If invalid, increment `malformed_lines` and continue.
3. Convert `bytes`: `0` if `"-"`, otherwise parsed 64-bit integer.
4. Update counters:
   - `total_requests += 1`
   - `total_bytes += bytes`
   - `status_classes["{status // 100}xx"] += 1`
   - `visitors[client_ip] += 1`
   - `paths[path] += 1`
   - `methods[method] += 1`

### 3.2 Post-Processing & Cross-Language Determinism

1. **Unique visitors:** `unique_visitors = len(visitors)`.
2. **Error count:** `error_count = status_classes["4xx"] + status_classes["5xx"]`.
3. **Error rate (`error_rate_percent`):**
   - If `total_requests == 0`, return `0.0`.
   - Otherwise, compute percentage rounded to 2 decimal places using **exact integer half-up rounding** (half away from zero for non-negative values):
     ```text
     numerator = error_count * 10000
     q = numerator // total_requests
     r = numerator % total_requests
     if 2 * r >= total_requests:
         q += 1
     error_rate_percent = q / 100.0
     ```
   - **Rationale:** Native `round()` differs across runtimes (`round()` in Python uses round-half-to-even, whereas `Math.round` in JS and `math.Round` in Go use half-away-from-zero, and floating-point division introduces binary representation drift on exact `.xx5` boundaries such as `1/32 = 3.125%`). Exact integer division before dividing by `100.0` guarantees identical outputs in every language.
4. **Top-K Ranking (`top_visitors`, `top_paths`):**
   - Sort entries by `requests` **descending**, breaking ties by key (`ip` or `path`) **lexicographically ascending** (bytewise / UTF-8 codepoint order, e.g., `"10.0.0.1" < "10.0.0.10" < "10.0.0.2"`).
   - Take at most the first `5` entries. Do NOT pad if fewer than `5` distinct items exist.
5. **Methods map (`methods`):**
   - Emit keys sorted lexicographically ascending for deterministic output diffs.

### 3.3 Complexity Targets
- **Time complexity:** $O(N + U \log U + P \log P)$ where $N$ is total lines, $U$ is unique visitors, and $P$ is unique paths (or $O(N + U \log 5 + P \log 5)$ using a bounded min-heap for Top-5).
- **Space complexity:** $O(U + P)$ resident memory, independent of input file size $N$.

---

## 4. Output Format

### 4.1 JSON Schema

```json
{
  "total_requests": 0,
  "malformed_lines": 0,
  "unique_visitors": 0,
  "total_bytes": 0,
  "error_count": 0,
  "error_rate_percent": 0.0,
  "status_classes": {
    "1xx": 0,
    "2xx": 0,
    "3xx": 0,
    "4xx": 0,
    "5xx": 0
  },
  "methods": {},
  "top_visitors": [
    { "ip": "192.168.1.1", "requests": 10 }
  ],
  "top_paths": [
    { "path": "/index.html", "requests": 10 }
  ]
}
```

### 4.2 Field Contract

| Field | JSON Type | Constraints / Notes |
| :--- | :--- | :--- |
| `total_requests` | Integer (`int64`) | Count of valid parsed log entries (`>= 0`). |
| `malformed_lines` | Integer (`int64`) | Count of non-blank lines that failed parsing/validation (`>= 0`). |
| `unique_visitors` | Integer (`int64`) | Count of distinct `client_ip` values across valid entries (`>= 0`). |
| `total_bytes` | Integer (`int64`) | Sum of response bytes across valid entries (`>= 0`). Must support `> 2^31 - 1` without 32-bit overflow. |
| `error_count` | Integer (`int64`) | `status_classes["4xx"] + status_classes["5xx"]`. |
| `error_rate_percent` | Number (`float64`) | Percentage in `[0.0, 100.0]`, rounded to 2 decimal places per Section 3.2. |
| `status_classes` | Object | Always includes all 5 keys `"1xx"`, `"2xx"`, `"3xx"`, `"4xx"`, `"5xx"` with integer counts. |
| `methods` | Object | Map of `method -> integer count`. Empty `{}` if `total_requests == 0`. |
| `top_visitors` | Array | Up to 5 objects `{"ip": string, "requests": integer}`. Empty `[]` (never `null`) if `total_requests == 0`. |
| `top_paths` | Array | Up to 5 objects `{"path": string, "requests": integer}`. Empty `[]` (never `null`) if `total_requests == 0`. |

> **Polyglot Test Assertion Rule:** Equivalence test runners MUST parse `stdout` as JSON and compare structured values numerically (so `0` and `0.0` for `error_rate_percent` compare equal, while all integer fields and array element orders match strictly).

---

## 5. Edge Cases

| Category | Scenario | Expected Behavior |
| :--- | :--- | :--- |
| Empty / Blank Input | 0-byte file or file containing only `\n`, `\r\n`, spaces, tabs | Exit `0`; all counts `0`, `error_rate_percent` `0.0`, `methods: {}`, `top_*: []`. |
| All Malformed | Every non-blank line fails grammar or range checks | Exit `0`; `total_requests: 0`, `malformed_lines: <N>`, `error_rate_percent: 0.0` (no division by zero). |
| Line Endings | Mixed `\n`, `\r\n`, and final line missing trailing newline | Final line processed identically; `\r` never leaks into `user_agent` or fails quote matching. |
| Bytes Dash & 64-bit | `bytes` field is `"-"`, `"0"`, or sums exceeding `2^31 - 1` | `"-"` adds `0`; sums above `2,147,483,647` accumulate accurately in 64-bit integers. |
| Escaped Quotes | `referer` or `user_agent` contains `\"` or `\\` | Parsed as valid line without splitting prematurely on inner quotes. |
| Request Variants | `OPTIONS * HTTP/1.1`, query strings (`/search?q=a&b=1`), `HTTP/2.0` | Accepted; query string preserved intact in `path` and `top_paths`. |
| Invalid Ranges | Status `99`/`600`, negative bytes `-10`, day `99`, hour `25`, lowercase method `get` | Rejected as malformed; `malformed_lines += 1`. |
| Tie-Breaking & `< 5` | Multiple IPs/paths with equal counts, or fewer than 5 unique keys | Sorted by `requests` DESC, then key ASCII/UTF-8 ASC; array length equals `min(5, unique_count)`. |
| Rounding Half-Up | `error_count / total_requests` lands on `.xx5%` (e.g., `1 / 32 = 3.125%`) | Rounds half away from zero (`3.13`, NOT `3.12` banker's rounding). |
| Invalid CLI Usage | Missing file arg, extra args, non-existent file, or directory path | Exit `1`, diagnostic message on `stderr`, empty `stdout`. |

---

## 6. Test Cases

### TC-01: Empty File (`tc01_empty.log`)
- **Purpose:** Verify baseline zero-state handling and no division by zero.
- **Input:** *(0 bytes / empty file)*
- **Exit Code:** `0`
- **Expected Output:**
```json
{
  "total_requests": 0,
  "malformed_lines": 0,
  "unique_visitors": 0,
  "total_bytes": 0,
  "error_count": 0,
  "error_rate_percent": 0.0,
  "status_classes": {
    "1xx": 0,
    "2xx": 0,
    "3xx": 0,
    "4xx": 0,
    "5xx": 0
  },
  "methods": {},
  "top_visitors": [],
  "top_paths": []
}
```

---

### TC-02: Whitespace-Only & CRLF Blank Lines (`tc02_whitespace_only.log`)
- **Purpose:** Verify CRLF and whitespace-only lines are ignored without counting as malformed.
- **Input (hex-equivalent lines):**
```text
\r\n
   \n
\t \r\n
```
- **Exit Code:** `0`
- **Expected Output:** Identical to `TC-01`.

---

### TC-03: Standard Mixed Traffic (`tc03_standard_mixed.log`)
- **Purpose:** Verify method breakdown, `2xx`/`3xx`/`4xx`/`5xx` classes, `bytes = "-"`, query-string retention, repeating error rate (`2/6 = 33.33%`), and top-5 path cutoff.
- **Input:**
```text
192.168.1.10 - alice [10/Nov/2026:10:00:01 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
192.168.1.11 - - [10/Nov/2026:10:00:02 +0000] "POST /api/login HTTP/1.1" 302 - "https://example.com/login" "curl/8.5.0"
192.168.1.10 - alice [10/Nov/2026:10:00:03 +0000] "GET /search?q=polyglot HTTP/1.1" 200 4096 "https://example.com/" "Mozilla/5.0"
10.0.0.5 - bob [10/Nov/2026:10:00:04 +0000] "GET /missing HTTP/1.1" 404 512 "-" "curl/8.5.0"
192.168.1.10 - alice [10/Nov/2026:10:00:05 +0000] "DELETE /api/session HTTP/1.1" 204 - "-" "Mozilla/5.0"
10.0.0.8 - - [10/Nov/2026:10:00:06 +0000] "GET /api/data HTTP/1.1" 502 256 "-" "python-requests/2.31.0"
```
- **Exit Code:** `0`
- **Expected Output:**
```json
{
  "total_requests": 6,
  "malformed_lines": 0,
  "unique_visitors": 4,
  "total_bytes": 5888,
  "error_count": 2,
  "error_rate_percent": 33.33,
  "status_classes": {
    "1xx": 0,
    "2xx": 3,
    "3xx": 1,
    "4xx": 1,
    "5xx": 1
  },
  "methods": {
    "DELETE": 1,
    "GET": 4,
    "POST": 1
  },
  "top_visitors": [
    { "ip": "192.168.1.10", "requests": 3 },
    { "ip": "10.0.0.5", "requests": 1 },
    { "ip": "10.0.0.8", "requests": 1 },
    { "ip": "192.168.1.11", "requests": 1 }
  ],
  "top_paths": [
    { "path": "/api/data", "requests": 1 },
    { "path": "/api/login", "requests": 1 },
    { "path": "/api/session", "requests": 1 },
    { "path": "/index.html", "requests": 1 },
    { "path": "/missing", "requests": 1 }
  ]
}
```

---

### TC-04: Malformed Lines, Escaped Quotes & `1xx` / `OPTIONS *` (`tc04_malformed_and_escapes.log`)
- **Purpose:** Verify strict validation of day/hour ranges, HTTP method casing, status bounds, negative bytes, unclosed quotes, alongside valid `OPTIONS *`, `101`, and `\"` escapes.
- **Input:**
```text
203.0.113.1 - - [10/Nov/2026:11:15:30 -0500] "OPTIONS * HTTP/1.1" 200 0 "-" "Custom \"Agent\" v1"
203.0.113.2 - - [10/Nov/2026:11:15:31 +0400] "GET /ws HTTP/1.1" 101 0 "-" "WebSocketClient/2.0"
203.0.113.1 - - [99/Nov/2026:11:15:32 +0000] "GET /bad-day HTTP/1.1" 200 100 "-" "curl/8.5.0"
203.0.113.1 - - [10/Nov/2026:25:15:32 +0000] "GET /bad-hour HTTP/1.1" 200 100 "-" "curl/8.5.0"
203.0.113.1 - - [10/Nov/2026:11:15:33 +0000] "get /lowercase HTTP/1.1" 200 100 "-" "curl/8.5.0"
203.0.113.1 - - [10/Nov/2026:11:15:34 +0000] "GET /bad-status HTTP/1.1" 600 100 "-" "curl/8.5.0"
203.0.113.1 - - [10/Nov/2026:11:15:35 +0000] "GET /neg-bytes HTTP/1.1" 200 -10 "-" "curl/8.5.0"
203.0.113.1 - - [10/Nov/2026:11:15:36 +0000] "GET /unclosed HTTP/1.1" 200 100 "-" "unclosed
completely malformed garbage line
```
- **Exit Code:** `0`
- **Expected Output:**
```json
{
  "total_requests": 2,
  "malformed_lines": 7,
  "unique_visitors": 2,
  "total_bytes": 0,
  "error_count": 0,
  "error_rate_percent": 0.0,
  "status_classes": {
    "1xx": 1,
    "2xx": 1,
    "3xx": 0,
    "4xx": 0,
    "5xx": 0
  },
  "methods": {
    "GET": 1,
    "OPTIONS": 1
  },
  "top_visitors": [
    { "ip": "203.0.113.1", "requests": 1 },
    { "ip": "203.0.113.2", "requests": 1 }
  ],
  "top_paths": [
    { "path": "*", "requests": 1 },
    { "path": "/ws", "requests": 1 }
  ]
}
```

---

### TC-05: Deterministic Tie-Breaking & Top-5 Cutoff (`tc05_tie_breaking.log`)
- **Purpose:** Verify lexicographical tie-breaking (`"10.0.0.1"` < `"10.0.0.10"` < `"10.0.0.2"`) and exact cutoff at 5 entries when 7 unique IPs and 7 unique paths exist.
- **Input:**
```text
10.0.0.2 - - [10/Nov/2026:12:00:01 +0000] "GET /z HTTP/1.1" 200 10 "-" "UA"
10.0.0.2 - - [10/Nov/2026:12:00:02 +0000] "GET /f HTTP/1.1" 200 10 "-" "UA"
10.0.0.10 - - [10/Nov/2026:12:00:03 +0000] "GET /b HTTP/1.1" 200 10 "-" "UA"
10.0.0.10 - - [10/Nov/2026:12:00:04 +0000] "GET /b HTTP/1.1" 200 10 "-" "UA"
10.0.0.1 - - [10/Nov/2026:12:00:05 +0000] "GET /a HTTP/1.1" 200 10 "-" "UA"
10.0.0.1 - - [10/Nov/2026:12:00:06 +0000] "GET /a HTTP/1.1" 200 10 "-" "UA"
10.0.0.3 - - [10/Nov/2026:12:00:07 +0000] "GET /c HTTP/1.1" 200 10 "-" "UA"
10.0.0.3 - - [10/Nov/2026:12:00:08 +0000] "GET /c HTTP/1.1" 200 10 "-" "UA"
10.0.0.4 - - [10/Nov/2026:12:00:09 +0000] "GET /d HTTP/1.1" 200 10 "-" "UA"
10.0.0.4 - - [10/Nov/2026:12:00:10 +0000] "GET /d HTTP/1.1" 200 10 "-" "UA"
10.0.0.5 - - [10/Nov/2026:12:00:11 +0000] "GET /e HTTP/1.1" 200 10 "-" "UA"
10.0.0.6 - - [10/Nov/2026:12:00:12 +0000] "GET /e HTTP/1.1" 200 10 "-" "UA"
```
- **Exit Code:** `0`
- **Expected Output:**
```json
{
  "total_requests": 12,
  "malformed_lines": 0,
  "unique_visitors": 7,
  "total_bytes": 120,
  "error_count": 0,
  "error_rate_percent": 0.0,
  "status_classes": {
    "1xx": 0,
    "2xx": 12,
    "3xx": 0,
    "4xx": 0,
    "5xx": 0
  },
  "methods": {
    "GET": 12
  },
  "top_visitors": [
    { "ip": "10.0.0.1", "requests": 2 },
    { "ip": "10.0.0.10", "requests": 2 },
    { "ip": "10.0.0.2", "requests": 2 },
    { "ip": "10.0.0.3", "requests": 2 },
    { "ip": "10.0.0.4", "requests": 2 }
  ],
  "top_paths": [
    { "path": "/a", "requests": 2 },
    { "path": "/b", "requests": 2 },
    { "path": "/c", "requests": 2 },
    { "path": "/d", "requests": 2 },
    { "path": "/e", "requests": 2 }
  ]
}
```

---

### TC-06: 64-Bit Byte Summation (`tc06_large_bytes.log`)
- **Purpose:** Verify `total_bytes` does not overflow signed 32-bit integer limits (`> 2,147,483,647`) and validates `HTTP/2.0`.
- **Input:**
```text
172.16.0.1 - - [10/Nov/2026:13:00:01 +0000] "GET /iso/ubuntu.iso HTTP/2.0" 200 2147483648 "-" "aria2/1.37"
172.16.0.2 - - [10/Nov/2026:13:00:02 +0000] "GET /iso/debian.iso HTTP/2.0" 200 3000000000 "-" "curl/8.5.0"
172.16.0.3 - - [10/Nov/2026:13:00:03 +0000] "GET /iso/missing.iso HTTP/2.0" 404 128 "-" "curl/8.5.0"
```
- **Exit Code:** `0`
- **Expected Output:**
```json
{
  "total_requests": 3,
  "malformed_lines": 0,
  "unique_visitors": 3,
  "total_bytes": 5147483776,
  "error_count": 1,
  "error_rate_percent": 33.33,
  "status_classes": {
    "1xx": 0,
    "2xx": 2,
    "3xx": 0,
    "4xx": 1,
    "5xx": 0
  },
  "methods": {
    "GET": 3
  },
  "top_visitors": [
    { "ip": "172.16.0.1", "requests": 1 },
    { "ip": "172.16.0.2", "requests": 1 },
    { "ip": "172.16.0.3", "requests": 1 }
  ],
  "top_paths": [
    { "path": "/iso/debian.iso", "requests": 1 },
    { "path": "/iso/missing.iso", "requests": 1 },
    { "path": "/iso/ubuntu.iso", "requests": 1 }
  ]
}
```

---

### TC-07: All Malformed Input (`tc07_all_malformed.log`)
- **Purpose:** Verify `total_requests == 0` with non-zero `malformed_lines` does not divide by zero.
- **Input:**
```text
not a log line
127.0.0.1 - - [10/Nov/2026:14:00:00 +0000] "GET /ok HTTP/1.1" 99 10 "-" "UA"
127.0.0.1 - - [10/Nov/2026:14:00:00 +0000] "GET relative/path HTTP/1.1" 200 10 "-" "UA"
127.0.0.1 - - [10/Nov/2026:14:00:00 +0000] "GET /ok HTTP/1.1" 200 abc "-" "UA"
```
- **Exit Code:** `0`
- **Expected Output:**
```json
{
  "total_requests": 0,
  "malformed_lines": 4,
  "unique_visitors": 0,
  "total_bytes": 0,
  "error_count": 0,
  "error_rate_percent": 0.0,
  "status_classes": {
    "1xx": 0,
    "2xx": 0,
    "3xx": 0,
    "4xx": 0,
    "5xx": 0
  },
  "methods": {},
  "top_visitors": [],
  "top_paths": []
}
```

---

### TC-08: Exact Half-Up Rounding Boundary (`tc08_rounding_half_up.log`)
- **Purpose:** Verify `1 / 32 = 3.125%` rounds half-up to `3.13` rather than Python's banker's rounding (`3.12`).
- **Input:**
```text
198.51.100.1 - - [10/Nov/2026:15:00:00 +0000] "GET /fail HTTP/1.1" 500 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:01 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:02 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:03 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:04 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:05 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:06 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:07 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:08 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:09 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:10 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:11 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:12 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:13 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:14 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:15 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:16 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:17 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:18 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:19 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:20 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:21 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:22 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:23 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:24 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:25 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:26 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:27 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:28 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:29 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:30 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
198.51.100.1 - - [10/Nov/2026:15:00:31 +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"
```
- **Exit Code:** `0`
- **Expected Output:**
```json
{
  "total_requests": 32,
  "malformed_lines": 0,
  "unique_visitors": 1,
  "total_bytes": 3200,
  "error_count": 1,
  "error_rate_percent": 3.13,
  "status_classes": {
    "1xx": 0,
    "2xx": 31,
    "3xx": 0,
    "4xx": 0,
    "5xx": 1
  },
  "methods": {
    "GET": 32
  },
  "top_visitors": [
    { "ip": "198.51.100.1", "requests": 32 }
  ],
  "top_paths": [
    { "path": "/ok", "requests": 31 },
    { "path": "/fail", "requests": 1 }
  ]
}
```

---

## 7. Implementation & Portability Checklist

When translating this specification across Python, Node.js/JavaScript, Go, Rust, or Java:
- **Streaming I/O:** Use buffered line readers (`open()` iterator / `readline` / `bufio.Scanner` with increased max token size if needed, or `bufio.Reader.ReadString('\n')` / `BufRead::lines` / `BufferedReader`). Note: Go's `bufio.Scanner` defaults to a 64 KiB line limit; prefer `bufio.Reader` or raise the buffer limit to handle long `User-Agent` / URL lines safely.
- **Integer Safety:** Use 64-bit integers (`int64`/`u64`) for `total_bytes`. In JavaScript, document `Number.MAX_SAFE_INTEGER` (`9,007,199,254,740,991` bytes ≈ 8 PiB), which comfortably exceeds practical single-host logs.
- **Regex vs. Zero-Allocation Scanner:** Compiled regexes are concise in Python/JS, whereas manual byte/slice scanning avoids backtracking and significantly improves throughput in Go and Rust—both are valid as long as every rule in Section 2 is enforced identically.
- **No Locale Dependencies:** Month matching (`Jan`..`Dec`) and lexicographical sorting MUST NOT depend on OS locale settings.
