# Bug Descriptions

## bug1.py
- **Intended Behavior**: Return the last `limit` event records from an event list in chronological order.
- **Current Issue**: Off-by-one error due to incorrect slicing index calculation (`offset = len(events) - limit - 1`), returning `limit + 1` elements instead of `limit`.

## bug2.js
- **Intended Behavior**: Recursively merge configuration objects from a source payload into a target configuration object.
- **Current Issue**: Prototype pollution vulnerability (CWE-1321) due to recursive traversal of `__proto__` properties, allowing attackers to mutate `Object.prototype` and escalate privileges.

## bug3.java
- **Intended Behavior**: Validate whether an incoming authentication token matches the configured master authorization token string.
- **Current Issue**: Reference identity comparison bug (CWE-595). Using the `==` operator on dynamic strings compares memory references rather than character values (`.equals()`), causing valid tokens to fail validation.

## bug4.py
- **Intended Behavior**: Safely query the database to retrieve user profile data for a specific username.
- **Current Issue**: SQL injection vulnerability (CWE-89 / OWASP A03:2021). The query string interpolates unsanitized user input directly via f-strings rather than using parameterized query placeholders, permitting query manipulation.

## bug5.js
- **Intended Behavior**: Asynchronously fetch metric records for an array of user IDs and resolve to an array of all collected metrics.
- **Current Issue**: Asynchronous execution bug. `Array.prototype.forEach` does not await async callback promises, resulting in the function returning an empty array before asynchronous operations resolve.

## bug6.c
- **Intended Behavior**: Allocate heap memory and construct a formatted user identifier string combining a username and formatted numeric identifier.
- **Current Issue**: Off-by-one buffer overflow (CWE-193 / CWE-120). The memory allocation `malloc(total_len)` omits the extra byte required for the terminating null character (`\0`), causing `strcat` to write past allocated heap boundaries.
