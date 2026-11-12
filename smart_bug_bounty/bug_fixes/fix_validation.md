# Fix Validation

## bug1_fixed.py
- **Target Fixed File**: `smart_bug_bounty/bug_fixes/bug1_fixed.py`
- **Original Bug Snippet**: `smart_bug_bounty/bug_snippets/bug1.py`
- **Original Issue**: Off-by-one error caused by `offset = len(events) - limit - 1`, which subtracted an extra index offset and returned `limit + 1` elements.
- **Fix Applied**: Implemented negative list slicing `events[-limit:]` for strict terminal boundary extraction when `limit < len(events)`.
- **Test Results**: All 3 test cases passed.
  - Test 1 (Standard): `fetch_latest_events(audit_log, 3)` returned exactly 3 items ending with ID 105. Status: PASS.
  - Test 2 (Zero Limit): `fetch_latest_events(audit_log, 0)` returned empty list `[]`. Status: PASS.
  - Test 3 (Exceeding Limit): `fetch_latest_events(audit_log, 10)` returned complete list of 5 elements without error. Status: PASS.
- **Runnable Evidence (stdout)**:
  ```
  Test 1 (Standard): PASS
  Test 2 (Zero Limit): PASS
  Test 3 (Exceeding Limit): PASS
  ```

## bug2_fixed.js
- **Target Fixed File**: `smart_bug_bounty/bug_fixes/bug2_fixed.js`
- **Original Bug Snippet**: `smart_bug_bounty/bug_snippets/bug2.js`
- **Original Issue**: Prototype pollution vulnerability (CWE-1321) allowing untrusted `__proto__` and constructor properties to mutate `Object.prototype`.
- **Fix Applied**: Implemented an explicit property key filter (`key === "__proto__" || key === "constructor" || key === "prototype"`) and defensive type checking during recursive merging.
- **Test Results**: All 3 test cases passed.
  - Test 1 (Prototype Pollution Prevention): Merged payload `{"__proto__": {"isAdmin": true}}` and confirmed `({}).isAdmin` remains undefined. Status: PASS.
  - Test 2 (Nested Merge): Merged `{ server: { port: 8080 } }` correctly into the target configuration. Status: PASS.
  - Test 3 (Null Source): Safely passed `null` source without throwing runtime exceptions. Status: PASS.
- **Runnable Evidence (stdout)**:
  ```
  Test 1 (Prototype Pollution Prevention): PASS
  Test 2 (Nested Merge): PASS
  Test 3 (Null Source): PASS
  ```

## bug3_fixed.java
- **Target Fixed File**: `smart_bug_bounty/bug_fixes/bug3_fixed.java`
- **Original Bug Snippet**: `smart_bug_bounty/bug_snippets/bug3.java`
- **Original Issue**: Reference identity comparison (`==`) on dynamic String objects (CWE-595). In `bug3.java`, the expression `sanitized == MASTER_TOKEN` checked memory references instead of character sequences. Even though `rawToken.trim()` produced the identical string content `"auth_tok_live_883921"`, the resulting `String` object resided at a separate heap memory address, causing reference equality to evaluate to `false`.
- **Fix Applied**: Replaced `sanitized == MASTER_TOKEN` with value comparison `MASTER_TOKEN.equals(sanitized)`. The method defensively guards against null, trims surrounding whitespace via `sanitized = rawToken.trim()`, and compares character sequences using `MASTER_TOKEN.equals(sanitized)`.
- **Test Results**: All 4 test cases passed.
  - Test 1 (Heap String): Input: `new String("auth_tok_live_883921")`, Expected: `true`, Actual: `true`. Status: PASS.
  - Test 2 (Padded String): Input: `"  auth_tok_live_883921  "`, Expected: `true`, Actual: `true`. Status: PASS.
  - Test 3 (Invalid Token): Input: `"invalid_token_999"`, Expected: `false`, Actual: `false`. Status: PASS.
  - Test 4 (Null Input): Input: `null`, Expected: `false`, Actual: `false`. Status: PASS.
- **Runnable Evidence (stdout)**:
  ```
  Test 1 (Heap String): PASS
  Test 2 (Padded String): PASS
  Test 3 (Invalid Token): PASS
  Test 4 (Null Input): PASS
  ```

## bug4_fixed.py
- **Target Fixed File**: `smart_bug_bounty/bug_fixes/bug4_fixed.py`
- **Original Bug Snippet**: `smart_bug_bounty/bug_snippets/bug4.py`
- **Original Issue**: SQL Injection vulnerability (CWE-89 / OWASP A03:2021) caused by direct f-string variable interpolation into the query string.
- **Fix Applied**: Switched to parameterized SQL execution using driver parameter placeholder `?` and passing parameters as a tuple `(username,)`.
- **Test Results**: All 3 test cases passed.
  - Test 1 (Legitimate Query): `find_user_by_username(cursor, "admin")` retrieved `(2, 'admin', 'administrator')`. Status: PASS.
  - Test 2 (SQL Injection Blocked): `find_user_by_username(cursor, "guest' OR role = 'administrator")` safely returned `None`. Status: PASS.
  - Test 3 (Nonexistent User): `find_user_by_username(cursor, "unknown_user")` safely returned `None`. Status: PASS.
- **Runnable Evidence (stdout)**:
  ```
  Test 1 (Legitimate Query): PASS
  Test 2 (SQL Injection Blocked): PASS
  Test 3 (Nonexistent User): PASS
  ```

## bug5_fixed.js
- **Target Fixed File**: `smart_bug_bounty/bug_fixes/bug5_fixed.js`
- **Original Bug Snippet**: `smart_bug_bounty/bug_snippets/bug5.js`
- **Original Issue**: Asynchronous execution defect in `Array.prototype.forEach` which does not await async callback promises, causing premature return of an empty array.
- **Fix Applied**: Replaced `forEach` with `Array.prototype.map` resolved concurrently through `Promise.all`.
- **Test Results**: All 3 test cases passed.
  - Test 1 (Multiple IDs): `fetchUserMetrics([1, 2, 3], mockApi)` resolved with all 3 metric objects. Status: PASS.
  - Test 2 (Single ID): `fetchUserMetrics([42], mockApi)` resolved with single metric object `[{ id: 42, score: 420 }]`. Status: PASS.
  - Test 3 (Empty Array): `fetchUserMetrics([], mockApi)` resolved immediately to empty array `[]`. Status: PASS.
- **Runnable Evidence (stdout)**:
  ```
  Test 1 (Multiple IDs): PASS
  Test 2 (Single ID): PASS
  Test 3 (Empty Array): PASS
  ```

## bug6_fixed.c
- **Target Fixed File**: `smart_bug_bounty/bug_fixes/bug6_fixed.c`
- **Original Bug Snippet**: `smart_bug_bounty/bug_snippets/bug6.c`
- **Original Issue**: Off-by-one heap buffer overflow (CWE-193 / CWE-120) omitting memory for the terminating null byte (`\0`) during `malloc`.
- **Fix Applied**: Allocated `total_len + 1` bytes and formatted numeric ID with `snprintf` specifying explicit buffer bounds.
- **Test Results**: All 3 test cases passed.
  - Test 1 (Standard Tag): Formatted `"developer"` and `42` into `"developer#0042"` with proper null termination. Status: PASS.
  - Test 2 (Empty Username): Formatted `""` and `1` into `"#0001"` safely. Status: PASS.
  - Test 3 (Large ID): Formatted `"admin"` and `9999` into `"admin#9999"` without buffer overflow. Status: PASS.
- **Runnable Evidence (stdout)**:
  ```
  Test 1 (Standard Tag): PASS
  Test 2 (Empty Username): PASS
  Test 3 (Large ID): PASS
  ```
