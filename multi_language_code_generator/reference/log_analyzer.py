"""Streaming HTTP Combined Log Format (CLF) analyzer reference implementation."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass
import json
from pathlib import Path
import re
import sys
from typing import Any

INT64_MAX = (1 << 63) - 1
TOP_K = 5

_LOG_PATTERN = re.compile(
    r"^(\S+) (\S+) (\S+) "
    r"\[(\d{2}/(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/\d{4}:\d{2}:\d{2}:\d{2} [+-]\d{4})\] "
    r'"([A-Z]+) (\S+) (HTTP/\d+\.\d+)" '
    r"(\d{3}) (-|\d+) "
    r'"((?:[^"\\]|\\.)*)" '
    r'"((?:[^"\\]|\\.)*)"$'
)


@dataclass(frozen=True, slots=True)
class LogEntry:
    """Validated fields extracted from a single Combined Log Format record."""

    client_ip: str
    method: str
    path: str
    status: int
    body_bytes: int


def is_blank_line(line: str) -> bool:
    """Return True if a line (after CRLF/LF stripping) contains only ASCII spaces or tabs."""
    return line.strip(" \t") == ""


def compute_error_rate_percent(error_count: int, total_requests: int) -> float:
    """Compute error rate percentage rounded half-up to 2 decimal places via integer arithmetic."""
    if total_requests == 0:
        return 0.0
    quotient, remainder = divmod(error_count * 10000, total_requests)
    if 2 * remainder >= total_requests:
        quotient += 1
    return quotient / 100.0


def _has_valid_timestamp_ranges(timestamp: str) -> bool:
    """Validate numeric bounds for DD/Mon/YYYY:HH:MM:SS [+-]ZZZZ."""
    day = int(timestamp[0:2])
    hour = int(timestamp[12:14])
    minute = int(timestamp[15:17])
    second = int(timestamp[18:20])
    return (
        1 <= day <= 31
        and 0 <= hour <= 23
        and 0 <= minute <= 59
        and 0 <= second <= 59
    )


class LogAnalyzer:
    """Single-pass streaming analyzer for Combined Log Format access logs."""

    def parse_line(self, raw_line: str) -> LogEntry | None:
        """Parse and validate one non-blank log line; return None when malformed."""
        line = raw_line.rstrip("\r\n")
        match = _LOG_PATTERN.match(line)
        if match is None:
            return None

        client_ip, _ident, _user, timestamp, method, path, _proto, status_str, bytes_str, _ref, _ua = (
            match.groups()
        )

        if not _has_valid_timestamp_ranges(timestamp):
            return None

        if not (path.startswith("/") or path == "*"):
            return None

        status = int(status_str)
        if not (100 <= status <= 599):
            return None

        if bytes_str == "-":
            body_bytes = 0
        else:
            body_bytes = int(bytes_str)
            if body_bytes > INT64_MAX:
                return None

        return LogEntry(
            client_ip=client_ip,
            method=method,
            path=path,
            status=status,
            body_bytes=body_bytes,
        )

    def analyze_stream(self, lines: Iterable[str]) -> dict[str, Any]:
        """Aggregate log metrics over an iterable of lines in O(N) streaming time."""
        total_requests = 0
        malformed_lines = 0
        total_bytes = 0
        status_classes = {
            "1xx": 0,
            "2xx": 0,
            "3xx": 0,
            "4xx": 0,
            "5xx": 0,
        }
        visitors: Counter[str] = Counter()
        paths: Counter[str] = Counter()
        methods: Counter[str] = Counter()

        for raw_line in lines:
            stripped = raw_line.rstrip("\r\n")
            if is_blank_line(stripped):
                continue

            entry = self.parse_line(stripped)
            if entry is None:
                malformed_lines += 1
                continue

            total_requests += 1
            total_bytes += entry.body_bytes
            status_classes[f"{entry.status // 100}xx"] += 1
            visitors[entry.client_ip] += 1
            paths[entry.path] += 1
            methods[entry.method] += 1

        error_count = status_classes["4xx"] + status_classes["5xx"]
        error_rate_percent = compute_error_rate_percent(error_count, total_requests)

        top_visitors = [
            {"ip": ip, "requests": count}
            for ip, count in sorted(visitors.items(), key=lambda item: (-item[1], item[0]))[:TOP_K]
        ]
        top_paths = [
            {"path": path, "requests": count}
            for path, count in sorted(paths.items(), key=lambda item: (-item[1], item[0]))[:TOP_K]
        ]

        return {
            "total_requests": total_requests,
            "malformed_lines": malformed_lines,
            "unique_visitors": len(visitors),
            "total_bytes": total_bytes,
            "error_count": error_count,
            "error_rate_percent": error_rate_percent,
            "status_classes": status_classes,
            "methods": dict(sorted(methods.items())),
            "top_visitors": top_visitors,
            "top_paths": top_paths,
        }

    def analyze_file(self, file_path: str | Path) -> dict[str, Any]:
        """Stream and analyze a UTF-8 log file line-by-line (replacing invalid UTF-8 bytes)."""
        path = Path(file_path)
        with path.open("r", encoding="utf-8", errors="replace", newline="\n") as handle:
            return self.analyze_stream(handle)


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint matching the cross-language specification."""
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("Usage: log_analyzer.py <input_file_path>", file=sys.stderr)
        return 1

    target = Path(args[0])
    if target.is_dir():
        print(f"Error: '{args[0]}' is a directory, expected a file.", file=sys.stderr)
        return 1

    analyzer = LogAnalyzer()
    try:
        report = analyzer.analyze_file(target)
    except OSError as exc:
        print(f"Error reading '{args[0]}': {exc}", file=sys.stderr)
        return 1

    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
