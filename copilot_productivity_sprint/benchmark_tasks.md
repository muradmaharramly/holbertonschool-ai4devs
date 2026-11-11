# Benchmark Tasks

## Sprint Design Rules

- **Time Box**: Each task is scoped for 15–30 minutes of implementation and verification.
- **Parity**: Both the manual (no-AI) run and the GitHub Copilot-assisted run must implement the exact same specification and pass the same automated test suite.
- **Zero External Infrastructure**: Tasks rely only on the verified runtimes documented in [`setup_notes.md`](./setup_notes.md) (Node.js `v24.12.0` and Python `3.12.2`) so timing is not skewed by database or third-party service setup.

---

## Task 1 - User CRUD Endpoint

**Requirements**:  
Implement an in-memory HTTP API server in Node.js (`node:http`) exposing `POST /users`, `GET /users/:id`, and `GET /users`.
- Validate incoming `Content-Type: application/json` and parse JSON safely without crashing on malformed payloads.
- Validate `name` (non-empty trimmed string, 2–100 characters) and `email` (trimmed string matching standard `local@domain.tld` format, normalized to lowercase).
- Enforce case-insensitive email uniqueness across stored users.
- Assign a unique string `id` (UUID via `node:crypto`) and ISO-8601 `createdAt` timestamp on creation.
- Export a server/app factory function so tests can bind to an ephemeral port (`0`) and reset state cleanly.

**Inputs**:  
- `POST /users`: JSON body `{ "name": "<string>", "email": "<string>" }`
- `GET /users/:id`: URL path parameter `id`
- `GET /users`: No request body

**Outputs**:  
- `POST /users` (`201 Created`): `{ "id": "<uuid>", "name": "<string>", "email": "<normalized_email>", "createdAt": "<iso8601>" }`
- `GET /users/:id` (`200 OK`): Stored user object matching `id`
- `GET /users` (`200 OK`): `{ "users": [ ... ], "count": <number> }`
- Error responses (`400`, `404`, `409`, `415`): `{ "error": "<descriptive_message>" }`

**Acceptance Criteria**:  
- Returns `201` with generated `id`, trimmed `name`, lowercase `email`, and `createdAt` on valid `POST /users`
- Returns `400` on missing fields, blank/short/oversized `name`, invalid `email` syntax, or malformed JSON body
- Returns `415` when `POST /users` is sent without `application/json` content type
- Returns `409` when `email` already exists (case-insensitive comparison, e.g., `Alice@Example.com` vs `alice@example.com`)
- Returns `200` with user record on `GET /users/:id`, or `404` when `id` does not exist
- Returns `404` for unknown routes or unsupported HTTP methods

---

## Task 2 - Log Stream Aggregator and Anomaly Summary

**Requirements**:  
Implement a Python module (`log_aggregator.py`) that parses newline-delimited JSON (NDJSON) HTTP access logs and computes per-service health metrics.
- Skip blank lines, validate required fields (`timestamp`, `service`, `endpoint`, `status`, `latency_ms`), and count malformed lines or invalid record types under `malformed_lines` instead of aborting the batch.
- Require `status` to be an integer in `100..599` and `latency_ms` to be a finite non-negative number (`int` or `float`, excluding `bool`).
- Group valid entries by `service` and compute:
  - `request_count` (int)
  - `error_count` (int, count of `status >= 500`)
  - `error_rate` (float, `error_count / request_count`, rounded to 4 decimal places)
  - `avg_latency_ms` (float, rounded to 2 decimal places)
  - `p95_latency_ms` (float, nearest-rank 95th percentile rounded to 2 decimal places)
  - `slowest_endpoint` (string, endpoint with highest average latency for that service; ties broken lexicographically)
- Sort the output service summaries by `error_rate` descending, then `request_count` descending, then `service` name ascending.

**Inputs**:  
- A string or iterable of NDJSON log lines, each expected to parse into `{ "timestamp": str, "service": str, "endpoint": str, "status": int, "latency_ms": float | int }`

**Outputs**:  
- Dictionary:
  ```json
  {
    "total_lines": 120,
    "valid_records": 118,
    "malformed_lines": 2,
    "services": [
      {
        "service": "payments",
        "request_count": 50,
        "error_count": 5,
        "error_rate": 0.1,
        "avg_latency_ms": 142.35,
        "p95_latency_ms": 410.0,
        "slowest_endpoint": "/v1/charge"
      }
    ]
  }
  ```

**Acceptance Criteria**:  
- Empty input returns `total_lines: 0`, `valid_records: 0`, `malformed_lines: 0`, and `services: []`
- Invalid JSON lines, missing required keys, boolean values passed as numbers, negative latencies, or out-of-range HTTP status codes increment `malformed_lines` without crashing
- Single-record service returns `p95_latency_ms` equal to that record's `latency_ms`
- `error_rate`, `avg_latency_ms`, and `p95_latency_ms` match exact nearest-rank percentile and rounding rules
- Service list ordering is deterministic across runs (error rate desc, request count desc, service name asc)

---

## Task 3 - Sliding-Window Rate Limiter

**Requirements**:  
Implement a deterministic in-memory sliding-window log rate limiter (`rate_limiter.py`) in Python.
- Configure the limiter with `max_requests: int` (`> 0`) and `window_seconds: float` (`> 0`), plus an optional injectable `clock: Callable[[], float]` (defaulting to `time.monotonic`) for deterministic testing without sleeps.
- Raise `ValueError` on non-positive `max_requests` or `window_seconds`, or on empty/whitespace-only client keys.
- Implement `allow(key: str) -> RateLimitDecision` (dataclass or named result) that:
  - Evicts timestamps outside the active sliding window (`timestamp <= now - window_seconds`).
  - Grants the request if active count `< max_requests`, records `now`, and reports remaining quota.
  - Rejects the request if active count `>= max_requests` without recording `now`, and computes `retry_after_seconds` as the remaining time until the oldest active timestamp expires.
- Implement `reset(key: str | None = None) -> None` to clear state for a single key or all keys, and `active_keys() -> int` to verify expired buckets are pruned and do not leak memory.

**Inputs**:  
- Constructor: `SlidingWindowRateLimiter(max_requests: int, window_seconds: float, clock: Callable[[], float] | None = None)`
- Method call: `allow(key: str)` where `key` identifies a client/API token

**Outputs**:  
- `RateLimitDecision` object with fields:
  - `allowed: bool`
  - `remaining: int` (`0` when rejected)
  - `limit: int`
  - `retry_after_seconds: float` (`0.0` when allowed; `> 0.0` when rejected, rounded to 3 decimal places)

**Acceptance Criteria**:  
- Constructor rejects `max_requests <= 0` or `window_seconds <= 0` (including booleans) with `ValueError`
- Empty or whitespace-only `key` raises `ValueError`
- Up to `max_requests` calls within `[t, t + window_seconds)` succeed with decrementing `remaining`; call `max_requests + 1` returns `allowed=False`, `remaining=0`, and accurate `retry_after_seconds`
- Advancing the injected clock to exactly `oldest_timestamp + window_seconds` evicts the oldest entry and allows a new request
- Rejected calls do not consume quota or extend the lockout window
- Different keys are strictly isolated, and expired empty key buckets are removed from internal storage
