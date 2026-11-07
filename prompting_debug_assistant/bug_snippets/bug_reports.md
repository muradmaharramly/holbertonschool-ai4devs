# Bug Reports

## Bug Report – bug1.py
- **Summary**: Off-by-one boundary calculation in loop range leading to an invalid slice on terminal iteration.
- **Root Cause**: The loop boundary was specified as `range(len(data) - window_size + 2)`, which ran one iteration too far. On the final iteration, the slice `data[4:7]` returned only 2 items instead of 3, calculating a partial window average and appending an unwanted extra element to the output list.
- **Resolution**: Changed the loop upper bound to `len(data) - window_size + 1` as recommended by AI. No manual code tweaks beyond the AI suggestion were necessary; verified that terminal windows produce the exact expected mathematical results.
- **Lesson Learned**: When computing sliding windows or array slices, calculate boundary indices using the formula `len(data) - window_size + 1` and verify with minimal sample arrays (`len == window_size`).

## Bug Report – bug2.js
- **Summary**: Unhandled null reference exception when accessing nested object properties.
- **Root Cause**: The code executed `parseFloat(tx.details.amount)` unconditionally. When processing records with `details: null`, the JavaScript engine threw `TypeError: Cannot read properties of null (reading 'amount')`, halting execution.
- **Resolution**: Adopted the AI suggestion to implement defensive validation `if (!tx || !tx.details || !tx.details.amount) return;`. Added a manual tweak to apply `Number.toFixed(2)` rounding on computed net balances to prevent IEEE-754 floating-point precision artifacts.
- **Lesson Learned**: Never assume external data payloads contain non-null nested structures; implement early defensive guards or optional chaining (`?.`) when traversing hierarchical objects.

## Bug Report – bug3.py
- **Summary**: Mutable default argument causing cross-invocation state leakage across distinct role groups.
- **Root Cause**: The parameter `members=[]` defined a mutable list as a default argument. In Python, default arguments are created once when the function definition is executed, meaning every invocation that omits `members` mutates and shares the identical list object in memory.
- **Resolution**: Implemented the AI-suggested sentinel pattern by setting the default parameter to `members=None` and assigning `members = []` inside the function body when `None`. Manually ensured `list(members)` creates a shallow defensive copy when an external iterable is supplied.
- **Lesson Learned**: In Python, always use `None` as the default argument for mutable collections (lists, dictionaries, sets) and initialize them dynamically inside the function body.

## Bug Report – bug4.js
- **Summary**: Lexicographical string sorting and string concatenation during numeric revenue accumulation.
- **Root Cause**: `Array.prototype.sort()` without a comparator converts elements to strings and sorts by UTF-16 code units (causing `100` to sort before `15` and `5.75`). Additionally, raw string representations like `"25.50"` caused the `+=` operator to perform string concatenation instead of numeric addition.
- **Resolution**: Combined the AI's suggested numeric comparator `.sort((a, b) => a - b)` with an upfront parsing step `products.map(p => parseFloat(p.price))` to enforce numeric typing before sorting and mathematical summation.
- **Lesson Learned**: In dynamically typed languages like JavaScript, always sanitize and coerce numerical string values to numbers immediately upon ingestion, and always supply an explicit comparator function to `.sort()`.

## Bug Report – bug5.c
- **Summary**: Missing statement terminator semicolon causing compilation failure in in-place string reversal.
- **Root Cause**: Line 6 contained `int len = strlen(str)` without a terminating semicolon, causing GCC to fail with syntax error `error: expected ';' before 'char'` at compile time.
- **Resolution**: Added the required semicolon to line 6 as identified by the AI assistant. Verified successful compilation with `gcc -Wall -Werror -Wextra -pedantic bug5_fixed.c`.
- **Lesson Learned**: Unlike modern interpreted languages with automatic semicolon insertion, C requires strict statement termination with semicolons; static analysis and compiler warning flags (`-Wall -Wextra`) immediately highlight missing terminators.

## Bug Report – bug6.py
- **Summary**: Runtime error caused by mutating dictionary size during iteration.
- **Root Cause**: Calling `del sessions[session_id]` directly inside a `for session_id, last_active in sessions.items():` loop mutated the dictionary while the iterator was active, raising `RuntimeError: dictionary changed size during iteration`.
- **Resolution**: Adopted the AI's suggestion to separate query from mutation by collecting expired keys into a list first via list comprehension: `expired = [sid for sid, last_active in sessions.items() if current_time - last_active > expiry_duration]`, followed by iterating through `expired` to delete entries from `sessions`.
- **Lesson Learned**: Never add or remove keys from a collection while directly iterating over its view; create a snapshot or collect targeted keys into a secondary list before applying mutations.
