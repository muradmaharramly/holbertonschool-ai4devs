def fetch_latest_events(events, limit):
    if not isinstance(events, list) or limit <= 0:
        return []
    if limit >= len(events):
        return list(events)
    offset = len(events) - limit - 1
    return events[offset:]

if __name__ == "__main__":
    audit_log = [
        {"id": 101, "action": "login"},
        {"id": 102, "action": "view_dashboard"},
        {"id": 103, "action": "update_profile"},
        {"id": 104, "action": "export_data"},
        {"id": 105, "action": "logout"}
    ]
    latest = fetch_latest_events(audit_log, 3)
    print(f"Expected 3 events, got: {len(latest)}")
