# Fix Validation

## bug1.py
- **Original Issue**: Off-by-one error caused by `offset = len(events) - limit - 1`, returning `limit + 1` elements.
- **Fix Applied**: Switched to negative list slice `events[-limit:]` for strict terminal boundary extraction.
- **Test Results**: All 3 test cases passed.
  - Test 1 (Standard): `fetch_latest_events(audit_log, 3)` returned exactly 3 items.
  - Test 2 (Empty/Zero): `fetch_latest_events(audit_log, 0)` returned empty list `[]`.
  - Test 3 (Exceeding limit): `fetch_latest_events(audit_log, 10)` returned complete list without error.

## bug2.js
- **Original Issue**: Prototype pollution (CWE-1321) allowing untrusted `__proto__` payloads to mutate `Object.prototype`.
- **Fix Applied**: Added key filter denying `__proto__`, `constructor`, and `prototype` during recursive merge.
- **Test Results**: All 3 test cases passed.
  - Test 1 (Pollution attempt): `mergeConfig(base, JSON.parse('{"__proto__": {"isAdmin": true}}'))` left `({}).isAdmin` undefined.
  - Test 2 (Valid nested object): Merged `{ server: { port: 8080 } }` correctly into base object.
  - Test 3 (Null/invalid source): Handled non-object and null source inputs safely without throwing exceptions.

## bug3.java
- **Original Issue**: Reference identity comparison (`==`) on dynamically allocated strings (CWE-595).
- **Fix Applied**: Replaced `==` reference operator with content comparison `MASTER_TOKEN.equals(sanitized)`.
- **Test Results**: All 3 test cases passed.
  - Test 1 (Heap instance): Validated `new String("auth_tok_live_883921")` returning `true`.
  - Test 2 (Padded string): Validated `"  auth_tok_live_883921  "` returning `true`.
  - Test 3 (Invalid token): Validated `"invalid_token_999"` returning `false`.

## bug4.py
- **Original Issue**: SQL Injection vulnerability (CWE-89 / OWASP A03:2021) via raw string interpolation.
- **Fix Applied**: Implemented parameterized query execution with driver placeholder `?` and tuple parameter binding.
- **Test Results**: All 3 test cases passed.
  - Test 1 (Legitimate query): `find_user_by_username(cursor, "admin")` returned `(2, 'admin', 'administrator')`.
  - Test 2 (Injection payload): `find_user_by_username(cursor, "guest' OR role = 'administrator")` safely returned `None`.
  - Test 3 (Nonexistent user): Querying unknown username safely returned `None`.

## bug5.js
- **Original Issue**: Asynchronous execution defect in `Array.prototype.forEach` returning an empty array before promises resolve.
- **Fix Applied**: Replaced `forEach` with `Array.prototype.map` resolved via `Promise.all`.
- **Test Results**: All 3 test cases passed.
  - Test 1 (Multiple IDs): `fetchUserMetrics([1, 2, 3], mockApi)` resolved with all 3 metric objects.
  - Test 2 (Single ID): `fetchUserMetrics([42], mockApi)` resolved with single metric object `[{ id: 42, score: 420 }]`.
  - Test 3 (Empty input): `fetchUserMetrics([], mockApi)` resolved immediately to empty array `[]`.

## bug6.c
- **Original Issue**: Off-by-one buffer overflow (CWE-193 / CWE-120) omitting null-terminator byte in `malloc`.
- **Fix Applied**: Allocated `total_len + 1` bytes and used `snprintf` with explicit buffer size boundaries.
- **Test Results**: All 3 test cases passed.
  - Test 1 (Standard string): Concatenated `"developer"` and `42` into properly terminated `"developer#0042"`.
  - Test 2 (Empty string): Handled empty string input safely, allocating `#0001` with proper null termination.
  - Test 3 (Memory management): Allocated buffer freed without heap corruption or memory leakage.
