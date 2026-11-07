# Bug Descriptions

## Bug 1 – bug1.py
**Intended Behavior**: Calculate the moving averages of a numerical series across a specified window size and return the list of averages.
**Issue Type**: Off-by-one or loop logic issue.
**Notes**: The loop range expression `range(len(data) - window_size + 2)` causes an off-by-one slice calculation beyond valid boundaries, producing truncated slices and incorrect average calculations on terminal elements.

## Bug 2 – bug2.js
**Intended Behavior**: Aggregate financial transaction records by category (credits and debits) and compute the net account balance from an array of transaction objects.
**Issue Type**: Runtime exception.
**Notes**: Accessing `tx.details.amount` without null-checking `tx.details` causes an unhandled `TypeError: Cannot read properties of null (reading 'amount')` when a transaction contains null or missing details.

## Bug 3 – bug3.py
**Intended Behavior**: Assign user accounts to distinct role-based permission groups and return the member roster for each group independently.
**Issue Type**: Logical error.
**Notes**: Defining `members=[]` as a default argument creates a shared mutable list across all function invocations, resulting in cross-group member contamination where users from prior calls persist into subsequent group rosters.

## Bug 4 – bug4.js
**Intended Behavior**: Parse product price records from mixed input types, sort prices in ascending numerical order, and compute accurate total revenue and median values.
**Issue Type**: Misuse of data types or libraries.
**Notes**: Calling `.sort()` without a numeric comparator sorts elements lexicographically as strings rather than numerically. In addition, unparsed string values cause the `+=` operator to perform string concatenation instead of numeric addition for total revenue calculation.

## Bug 5 – bug5.c
**Intended Behavior**: Reverse the characters of a given null-terminated C string in-place using two-pointer swapping and print the reversed string.
**Issue Type**: Syntax error.
**Notes**: Line 6 contains a missing semicolon delimiter at the end of the declaration `int len = strlen(str)`, which causes the C compiler to fail with a syntax error (`expected ';' before 'char'`).

## Bug 6 – bug6.py
**Intended Behavior**: Filter out and remove expired user session entries from an active session dictionary based on an inactivity timeout threshold.
**Issue Type**: Off-by-one or loop logic issue.
**Notes**: Deleting dictionary keys with `del sessions[session_id]` directly while iterating over `sessions.items()` causes Python to raise a `RuntimeError: dictionary changed size during iteration`.
