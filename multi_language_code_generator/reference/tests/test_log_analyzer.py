"""Unit and CLI tests verifying the Python reference implementation against cross_language_spec.md."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

REFERENCE_DIR = Path(__file__).resolve().parent.parent
if str(REFERENCE_DIR) not in sys.path:
    sys.path.insert(0, str(REFERENCE_DIR))

from log_analyzer import INT64_MAX, LogAnalyzer, compute_error_rate_percent  # noqa: E402

CLI_SCRIPT = REFERENCE_DIR / "log_analyzer.py"


def _zero_report(malformed_lines: int = 0) -> dict:
    return {
        "total_requests": 0,
        "malformed_lines": malformed_lines,
        "unique_visitors": 0,
        "total_bytes": 0,
        "error_count": 0,
        "error_rate_percent": 0.0,
        "status_classes": {
            "1xx": 0,
            "2xx": 0,
            "3xx": 0,
            "4xx": 0,
            "5xx": 0,
        },
        "methods": {},
        "top_visitors": [],
        "top_paths": [],
    }


class TestLogAnalyzer(unittest.TestCase):
    """Contract tests for LogAnalyzer and its CLI."""

    def setUp(self) -> None:
        self.analyzer = LogAnalyzer()
        self._tmp_dir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp_dir.name)

    def tearDown(self) -> None:
        self._tmp_dir.cleanup()

    def _write_bytes(self, name: str, payload: bytes) -> Path:
        target = self.tmp_path / name
        target.write_bytes(payload)
        return target

    def _write_lines(self, name: str, lines: list[str], newline: str = "\n") -> Path:
        content = newline.join(lines) + (newline if lines else "")
        return self._write_bytes(name, content.encode("utf-8"))

    def _run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CLI_SCRIPT), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

    def test_tc01_empty_file(self) -> None:
        log_file = self._write_bytes("tc01_empty.log", b"")
        self.assertEqual(self.analyzer.analyze_file(log_file), _zero_report())

    def test_tc02_whitespace_and_crlf_blank_lines(self) -> None:
        log_file = self._write_bytes("tc02_whitespace.log", b"\r\n   \n\t \r\n")
        self.assertEqual(self.analyzer.analyze_file(log_file), _zero_report())

    def test_tc03_standard_mixed_traffic(self) -> None:
        lines = [
            '192.168.1.10 - alice [10/Nov/2026:10:00:01 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"',
            '192.168.1.11 - - [10/Nov/2026:10:00:02 +0000] "POST /api/login HTTP/1.1" 302 - "https://example.com/login" "curl/8.5.0"',
            '192.168.1.10 - alice [10/Nov/2026:10:00:03 +0000] "GET /search?q=polyglot HTTP/1.1" 200 4096 "https://example.com/" "Mozilla/5.0"',
            '10.0.0.5 - bob [10/Nov/2026:10:00:04 +0000] "GET /missing HTTP/1.1" 404 512 "-" "curl/8.5.0"',
            '192.168.1.10 - alice [10/Nov/2026:10:00:05 +0000] "DELETE /api/session HTTP/1.1" 204 - "-" "Mozilla/5.0"',
            '10.0.0.8 - - [10/Nov/2026:10:00:06 +0000] "GET /api/data HTTP/1.1" 502 256 "-" "python-requests/2.31.0"',
        ]
        expected = {
            "total_requests": 6,
            "malformed_lines": 0,
            "unique_visitors": 4,
            "total_bytes": 5888,
            "error_count": 2,
            "error_rate_percent": 33.33,
            "status_classes": {"1xx": 0, "2xx": 3, "3xx": 1, "4xx": 1, "5xx": 1},
            "methods": {"DELETE": 1, "GET": 4, "POST": 1},
            "top_visitors": [
                {"ip": "192.168.1.10", "requests": 3},
                {"ip": "10.0.0.5", "requests": 1},
                {"ip": "10.0.0.8", "requests": 1},
                {"ip": "192.168.1.11", "requests": 1},
            ],
            "top_paths": [
                {"path": "/api/data", "requests": 1},
                {"path": "/api/login", "requests": 1},
                {"path": "/api/session", "requests": 1},
                {"path": "/index.html", "requests": 1},
                {"path": "/missing", "requests": 1},
            ],
        }
        log_file = self._write_lines("tc03_standard.log", lines)
        self.assertEqual(self.analyzer.analyze_file(log_file), expected)

    def test_tc04_malformed_lines_and_escaped_quotes(self) -> None:
        lines = [
            '203.0.113.1 - - [10/Nov/2026:11:15:30 -0500] "OPTIONS * HTTP/1.1" 200 0 "-" "Custom \\"Agent\\" v1"',
            '203.0.113.2 - - [10/Nov/2026:11:15:31 +0400] "GET /ws HTTP/1.1" 101 0 "-" "WebSocketClient/2.0"',
            '203.0.113.1 - - [99/Nov/2026:11:15:32 +0000] "GET /bad-day HTTP/1.1" 200 100 "-" "curl/8.5.0"',
            '203.0.113.1 - - [10/Nov/2026:25:15:32 +0000] "GET /bad-hour HTTP/1.1" 200 100 "-" "curl/8.5.0"',
            '203.0.113.1 - - [10/Nov/2026:11:15:33 +0000] "get /lowercase HTTP/1.1" 200 100 "-" "curl/8.5.0"',
            '203.0.113.1 - - [10/Nov/2026:11:15:34 +0000] "GET /bad-status HTTP/1.1" 600 100 "-" "curl/8.5.0"',
            '203.0.113.1 - - [10/Nov/2026:11:15:35 +0000] "GET /neg-bytes HTTP/1.1" 200 -10 "-" "curl/8.5.0"',
            '203.0.113.1 - - [10/Nov/2026:11:15:36 +0000] "GET /unclosed HTTP/1.1" 200 100 "-" "unclosed',
            "completely malformed garbage line",
        ]
        expected = {
            "total_requests": 2,
            "malformed_lines": 7,
            "unique_visitors": 2,
            "total_bytes": 0,
            "error_count": 0,
            "error_rate_percent": 0.0,
            "status_classes": {"1xx": 1, "2xx": 1, "3xx": 0, "4xx": 0, "5xx": 0},
            "methods": {"GET": 1, "OPTIONS": 1},
            "top_visitors": [
                {"ip": "203.0.113.1", "requests": 1},
                {"ip": "203.0.113.2", "requests": 1},
            ],
            "top_paths": [
                {"path": "*", "requests": 1},
                {"path": "/ws", "requests": 1},
            ],
        }
        log_file = self._write_lines("tc04_malformed.log", lines)
        self.assertEqual(self.analyzer.analyze_file(log_file), expected)

    def test_tc05_tie_breaking_and_top_5_cutoff(self) -> None:
        lines = [
            '10.0.0.2 - - [10/Nov/2026:12:00:01 +0000] "GET /z HTTP/1.1" 200 10 "-" "UA"',
            '10.0.0.2 - - [10/Nov/2026:12:00:02 +0000] "GET /f HTTP/1.1" 200 10 "-" "UA"',
            '10.0.0.10 - - [10/Nov/2026:12:00:03 +0000] "GET /b HTTP/1.1" 200 10 "-" "UA"',
            '10.0.0.10 - - [10/Nov/2026:12:00:04 +0000] "GET /b HTTP/1.1" 200 10 "-" "UA"',
            '10.0.0.1 - - [10/Nov/2026:12:00:05 +0000] "GET /a HTTP/1.1" 200 10 "-" "UA"',
            '10.0.0.1 - - [10/Nov/2026:12:00:06 +0000] "GET /a HTTP/1.1" 200 10 "-" "UA"',
            '10.0.0.3 - - [10/Nov/2026:12:00:07 +0000] "GET /c HTTP/1.1" 200 10 "-" "UA"',
            '10.0.0.3 - - [10/Nov/2026:12:00:08 +0000] "GET /c HTTP/1.1" 200 10 "-" "UA"',
            '10.0.0.4 - - [10/Nov/2026:12:00:09 +0000] "GET /d HTTP/1.1" 200 10 "-" "UA"',
            '10.0.0.4 - - [10/Nov/2026:12:00:10 +0000] "GET /d HTTP/1.1" 200 10 "-" "UA"',
            '10.0.0.5 - - [10/Nov/2026:12:00:11 +0000] "GET /e HTTP/1.1" 200 10 "-" "UA"',
            '10.0.0.6 - - [10/Nov/2026:12:00:12 +0000] "GET /e HTTP/1.1" 200 10 "-" "UA"',
        ]
        expected = {
            "total_requests": 12,
            "malformed_lines": 0,
            "unique_visitors": 7,
            "total_bytes": 120,
            "error_count": 0,
            "error_rate_percent": 0.0,
            "status_classes": {"1xx": 0, "2xx": 12, "3xx": 0, "4xx": 0, "5xx": 0},
            "methods": {"GET": 12},
            "top_visitors": [
                {"ip": "10.0.0.1", "requests": 2},
                {"ip": "10.0.0.10", "requests": 2},
                {"ip": "10.0.0.2", "requests": 2},
                {"ip": "10.0.0.3", "requests": 2},
                {"ip": "10.0.0.4", "requests": 2},
            ],
            "top_paths": [
                {"path": "/a", "requests": 2},
                {"path": "/b", "requests": 2},
                {"path": "/c", "requests": 2},
                {"path": "/d", "requests": 2},
                {"path": "/e", "requests": 2},
            ],
        }
        log_file = self._write_lines("tc05_ties.log", lines)
        self.assertEqual(self.analyzer.analyze_file(log_file), expected)

    def test_tc06_large_bytes_int64_sum(self) -> None:
        lines = [
            '172.16.0.1 - - [10/Nov/2026:13:00:01 +0000] "GET /iso/ubuntu.iso HTTP/2.0" 200 2147483648 "-" "aria2/1.37"',
            '172.16.0.2 - - [10/Nov/2026:13:00:02 +0000] "GET /iso/debian.iso HTTP/2.0" 200 3000000000 "-" "curl/8.5.0"',
            '172.16.0.3 - - [10/Nov/2026:13:00:03 +0000] "GET /iso/missing.iso HTTP/2.0" 404 128 "-" "curl/8.5.0"',
        ]
        expected = {
            "total_requests": 3,
            "malformed_lines": 0,
            "unique_visitors": 3,
            "total_bytes": 5147483776,
            "error_count": 1,
            "error_rate_percent": 33.33,
            "status_classes": {"1xx": 0, "2xx": 2, "3xx": 0, "4xx": 1, "5xx": 0},
            "methods": {"GET": 3},
            "top_visitors": [
                {"ip": "172.16.0.1", "requests": 1},
                {"ip": "172.16.0.2", "requests": 1},
                {"ip": "172.16.0.3", "requests": 1},
            ],
            "top_paths": [
                {"path": "/iso/debian.iso", "requests": 1},
                {"path": "/iso/missing.iso", "requests": 1},
                {"path": "/iso/ubuntu.iso", "requests": 1},
            ],
        }
        log_file = self._write_lines("tc06_large.log", lines)
        self.assertEqual(self.analyzer.analyze_file(log_file), expected)

    def test_tc07_all_malformed_no_zero_division(self) -> None:
        lines = [
            "not a log line",
            '127.0.0.1 - - [10/Nov/2026:14:00:00 +0000] "GET /ok HTTP/1.1" 99 10 "-" "UA"',
            '127.0.0.1 - - [10/Nov/2026:14:00:00 +0000] "GET relative/path HTTP/1.1" 200 10 "-" "UA"',
            '127.0.0.1 - - [10/Nov/2026:14:00:00 +0000] "GET /ok HTTP/1.1" 200 abc "-" "UA"',
        ]
        log_file = self._write_lines("tc07_all_malformed.log", lines)
        self.assertEqual(self.analyzer.analyze_file(log_file), _zero_report(malformed_lines=4))

    def test_tc08_rounding_half_up_boundary(self) -> None:
        lines = [
            '198.51.100.1 - - [10/Nov/2026:15:00:00 +0000] "GET /fail HTTP/1.1" 500 100 "-" "probe/1.0"',
            *[
                f'198.51.100.1 - - [10/Nov/2026:15:00:{sec:02d} +0000] "GET /ok HTTP/1.1" 200 100 "-" "probe/1.0"'
                for sec in range(1, 32)
            ],
        ]
        expected = {
            "total_requests": 32,
            "malformed_lines": 0,
            "unique_visitors": 1,
            "total_bytes": 3200,
            "error_count": 1,
            "error_rate_percent": 3.13,
            "status_classes": {"1xx": 0, "2xx": 31, "3xx": 0, "4xx": 0, "5xx": 1},
            "methods": {"GET": 32},
            "top_visitors": [{"ip": "198.51.100.1", "requests": 32}],
            "top_paths": [
                {"path": "/ok", "requests": 31},
                {"path": "/fail", "requests": 1},
            ],
        }
        log_file = self._write_lines("tc08_rounding.log", lines)
        self.assertEqual(self.analyzer.analyze_file(log_file), expected)

    def test_compute_error_rate_percent_half_up_cases(self) -> None:
        self.assertEqual(compute_error_rate_percent(0, 0), 0.0)
        self.assertEqual(compute_error_rate_percent(1, 32), 3.13)
        self.assertEqual(compute_error_rate_percent(1, 8), 12.5)
        self.assertEqual(compute_error_rate_percent(2, 3), 66.67)
        self.assertEqual(compute_error_rate_percent(1, 1), 100.0)

    def test_crlf_and_missing_trailing_newline(self) -> None:
        payload = (
            '10.0.0.1 - - [10/Nov/2026:16:00:00 +0000] "GET /one HTTP/1.1" 200 10 "-" "UA"\r\n'
            '10.0.0.2 - - [10/Nov/2026:16:00:01 +0000] "HEAD /two HTTP/1.1" 200 0 "-" "UA"'
        ).encode("utf-8")
        log_file = self._write_bytes("no_eol.log", payload)
        report = self.analyzer.analyze_file(log_file)
        self.assertEqual(report["total_requests"], 2)
        self.assertEqual(report["malformed_lines"], 0)
        self.assertEqual(report["methods"], {"GET": 1, "HEAD": 1})

    def test_invalid_utf8_bytes_replaced_without_crash(self) -> None:
        payload = (
            b'10.0.0.1 - - [10/Nov/2026:16:05:00 +0000] "GET /utf8 HTTP/1.1" 200 42 "-" "bad\xff\xfeua"\n'
        )
        log_file = self._write_bytes("invalid_utf8.log", payload)
        report = self.analyzer.analyze_file(log_file)
        self.assertEqual(report["total_requests"], 1)
        self.assertEqual(report["malformed_lines"], 0)
        self.assertEqual(report["total_bytes"], 42)

    def test_int64_bytes_boundary_and_overflow_rejection(self) -> None:
        lines = [
            f'10.0.0.1 - - [10/Nov/2026:17:00:00 +0000] "GET /max HTTP/1.1" 200 {INT64_MAX} "-" "UA"',
            f'10.0.0.1 - - [10/Nov/2026:17:00:01 +0000] "GET /overflow HTTP/1.1" 200 {INT64_MAX + 1} "-" "UA"',
        ]
        report = self.analyzer.analyze_stream(lines)
        self.assertEqual(report["total_requests"], 1)
        self.assertEqual(report["malformed_lines"], 1)
        self.assertEqual(report["total_bytes"], INT64_MAX)

    def test_empty_quoted_strings_and_escaped_backslash(self) -> None:
        lines = [
            '10.0.0.1 - - [10/Nov/2026:17:10:00 +0000] "PUT /item HTTP/1.1" 201 15 "" "trail\\\\"',
            '10.0.0.1 - - [10/Nov/2026:17:10:01 +0000] "PATCH /item HTTP/1.1" 200 5 "" ""',
        ]
        report = self.analyzer.analyze_stream(lines)
        self.assertEqual(report["total_requests"], 2)
        self.assertEqual(report["malformed_lines"], 0)
        self.assertEqual(report["methods"], {"PATCH": 1, "PUT": 1})

    def test_cli_valid_file_outputs_json_and_zero_exit(self) -> None:
        log_file = self._write_lines(
            "cli_valid.log",
            ['192.0.2.1 - - [10/Nov/2026:18:00:00 +0000] "GET /health HTTP/1.1" 200 12 "-" "curl/8.5.0"'],
        )
        proc = self._run_cli(str(log_file))
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stderr, "")
        parsed = json.loads(proc.stdout)
        self.assertEqual(parsed["total_requests"], 1)
        self.assertEqual(parsed["total_bytes"], 12)

    def test_cli_invalid_argument_counts_return_one(self) -> None:
        for argv in ((), ("a.log", "b.log")):
            proc = self._run_cli(*argv)
            self.assertEqual(proc.returncode, 1)
            self.assertEqual(proc.stdout, "")
            self.assertTrue(proc.stderr.strip())

    def test_cli_missing_file_and_directory_return_one(self) -> None:
        missing = self.tmp_path / "does_not_exist.log"
        for target in (missing, self.tmp_path):
            proc = self._run_cli(str(target))
            self.assertEqual(proc.returncode, 1)
            self.assertEqual(proc.stdout, "")
            self.assertTrue(proc.stderr.strip())


if __name__ == "__main__":
    unittest.main()
