def fetch_latest_events(events, limit):
    if not isinstance(events, list) or limit <= 0:
        return []
    if limit >= len(events):
        return list(events)
    return events[-limit:]

if __name__ == "__main__":
    audit_log = [
        {"id": 101, "action": "login"},
        {"id": 102, "action": "view_dashboard"},
        {"id": 103, "action": "update_profile"},
        {"id": 104, "action": "export_data"},
        {"id": 105, "action": "logout"}
    ]
    t1 = fetch_latest_events(audit_log, 3)
    print(f"Test 1 (Standard): {'PASS' if len(t1) == 3 and t1[-1]['id'] == 105 else 'FAIL'}")

    t2 = fetch_latest_events(audit_log, 0)
    print(f"Test 2 (Zero Limit): {'PASS' if t2 == [] else 'FAIL'}")

    t3 = fetch_latest_events(audit_log, 10)
    print(f"Test 3 (Exceeding Limit): {'PASS' if len(t3) == 5 else 'FAIL'}")
