import time

def purge_expired_sessions(sessions, current_time, expiry_duration):
    expired = [
        sid for sid, last_active in sessions.items()
        if current_time - last_active > expiry_duration
    ]
    
    for session_id in expired:
        del sessions[session_id]
            
    return sessions

active_sessions = {
    "sess_101": 1700000000,
    "sess_102": 1700000500,
    "sess_103": 1700000100,
    "sess_104": 1700000800
}

current_timestamp = 1700000600
timeout = 300

remaining = purge_expired_sessions(active_sessions, current_timestamp, timeout)
print(remaining)
