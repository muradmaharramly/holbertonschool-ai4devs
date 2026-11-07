# Fix Validation

## Bug 1 – bug1_fixed.py
- **Input**: data = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0], window_size = 3
- **Expected Output**: [20.0, 30.0, 40.0, 50.0]
- **Actual Output**: [20.0, 30.0, 40.0, 50.0] ✅
- **Manual Tweaks**: None. The loop upper bound adjustment `len(data) - window_size + 1` resolves the off-by-one error cleanly.

## Bug 2 – bug2_fixed.js
- **Input**: [{ type: "credit", details: { amount: "150.50" } }, { type: "debit", details: null }, { type: "credit", details: { amount: "89.20" } }]
- **Expected Output**: { totalCredits: 239.7, totalDebits: 0, transactionCount: 3, netBalance: 239.7 }
- **Actual Output**: { totalCredits: 239.7, totalDebits: 0, transactionCount: 3, netBalance: 239.7 } ✅
- **Manual Tweaks**: Applied `Number.toFixed(2)` rounding on totals to avoid floating point precision artifacts on currency calculations.

## Bug 3 – bug3_fixed.py
- **Input**: assign_role_group("Administrators", ["alice", "bob"]), assign_role_group("Editors", ["charlie"]), assign_role_group("Viewers", ["dave", "alice"])
- **Expected Output**: Administrators: ['alice', 'bob'] (count: 2); Editors: ['charlie'] (count: 1); Viewers: ['dave', 'alice'] (count: 2)
- **Actual Output**: Administrators: ['alice', 'bob'] (count: 2); Editors: ['charlie'] (count: 1); Viewers: ['dave', 'alice'] (count: 2) ✅
- **Manual Tweaks**: None. Initializing `members = []` when `members is None` prevents mutable default state sharing across calls.

## Bug 4 – bug4_fixed.js
- **Input**: [{ name: "Widget", price: "25.50" }, { name: "Gadget", price: 100.00 }, { name: "Cable", price: "5.75" }, { name: "Adapter", price: 15.00 }]
- **Expected Output**: { sortedPrices: [5.75, 15, 25.5, 100], totalRevenue: 146.25, medianPrice: 25.5 }
- **Actual Output**: { sortedPrices: [5.75, 15, 25.5, 100], totalRevenue: 146.25, medianPrice: 25.5 } ✅
- **Manual Tweaks**: Added `parseFloat` in mapping stage to guarantee all values are typed as numbers before sorting and accumulation.

## Bug 5 – bug5_fixed.c
- **Input**: String "holberton" passed to reverse_string
- **Expected Output**: Reversed: notrebloh
- **Actual Output**: Reversed: notrebloh ✅
- **Manual Tweaks**: None. Appending terminating semicolon on line 6 resolves compilation failure.

## Bug 6 – bug6_fixed.py
- **Input**: sessions = {"sess_101": 1700000000, "sess_102": 1700000500, "sess_103": 1700000100, "sess_104": 1700000800}, current_timestamp = 1700000600, timeout = 300
- **Expected Output**: {'sess_102': 1700000500, 'sess_104': 1700000800}
- **Actual Output**: {'sess_102': 1700000500, 'sess_104': 1700000800} ✅
- **Manual Tweaks**: None. Collecting expired keys in a list comprehension before deletion prevents dictionary mutation during iteration.
