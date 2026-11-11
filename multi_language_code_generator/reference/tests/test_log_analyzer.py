"""Unit and CLI tests verifying the Python reference implementation against cross_language_spec.md."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

TESTS_DIR = Path(__file__).resolve().parent
REFERENCE_DIR = TESTS_DIR.parent
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

    def _run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CLI_SCRIPT), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

    def test_tc01_empty_file(self) -> None:
        self.assertEqual(self.analyzer.analyze_file(TESTS_DIR / "tc01_empty.log"), _zero_report())

    def test_tc02_whitespace_and_crlf_blank_lines(self) -> None:
        self.assertEqual(
            self.analyzer.analyze_file(TESTS_DIR / "tc02_whitespace_crlf.log"),
            _zero_report(),
        )

    def test_tc03_standard_mixed_traffic(self) -> None:
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
        self.assertEqual(
            self.analyzer.analyze_file(TESTS_DIR / "tc03_standard_mixed.log"),
            expected,
        )

    def test_tc04_malformed_lines_and_escaped_quotes(self) -> None:
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
        self.assertEqual(
            self.analyzer.analyze_file(TESTS_DIR / "tc04_malformed_and_escapes.log"),
            expected,
        )

    def test_tc05_tie_breaking_and_top_5_cutoff(self) -> None:
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
        self.assertEqual(
            self.analyzer.analyze_file(TESTS_DIR / "tc05_tie_breaking.log"),
            expected,
        )

    def test_tc06_large_bytes_int64_sum(self) -> None:
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
        self.assertEqual(
            self.analyzer.analyze_file(TESTS_DIR / "tc06_large_bytes.log"),
            expected,
        )

    def test_tc07_all_malformed_no_zero_division(self) -> None:
        self.assertEqual(
            self.analyzer.analyze_file(TESTS_DIR / "tc07_all_malformed.log"),
            _zero_report(malformed_lines=4),
        )

    def test_tc08_rounding_half_up_boundary(self) -> None:
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
        self.assertEqual(
            self.analyzer.analyze_file(TESTS_DIR / "tc08_rounding_half_up.log"),
            expected,
        )

    def test_tc09_crlf_and_missing_trailing_newline(self) -> None:
        report = self.analyzer.analyze_file(TESTS_DIR / "tc09_no_trailing_newline.log")
        self.assertEqual(report["total_requests"], 2)
        self.assertEqual(report["malformed_lines"], 0)
        self.assertEqual(report["methods"], {"GET": 1, "HEAD": 1})

    def test_tc10_invalid_utf8_bytes_replaced_without_crash(self) -> None:
        report = self.analyzer.analyze_file(TESTS_DIR / "tc10_invalid_utf8.log")
        self.assertEqual(report["total_requests"], 1)
        self.assertEqual(report["malformed_lines"], 0)
        self.assertEqual(report["total_bytes"], 42)

    def test_compute_error_rate_percent_half_up_cases(self) -> None:
        self.assertEqual(compute_error_rate_percent(0, 0), 0.0)
        self.assertEqual(compute_error_rate_percent(1, 32), 3.13)
        self.assertEqual(compute_error_rate_percent(1, 8), 12.5)
        self.assertEqual(compute_error_rate_percent(2, 3), 66.67)
        self.assertEqual(compute_error_rate_percent(1, 1), 100.0)

    def test_int64_bytes_boundary_and_overflow_rejection(self) -> None:
        lines = [
            f'10.0.0.1 - - [10/Nov/2026:17:00:00 +0000] "GET /max HTTP/1.1" 200 {INT64_MAX} "-" "UA"',
            f'10.0.0.1 - - [10/Nov/2026:17:00:01 +0000] "GET /overflow HTTP/1.1" 200 {INT64_MAX + 1} "-" "UA"',
        ]
        report = self.analyzer.analyze(lines)
        self.assertEqual(report["total_requests"], 1)
        self.assertEqual(report["malformed_lines"], 1)
        self.assertEqual(report["total_bytes"], INT64_MAX)

    def test_empty_quoted_strings_and_escaped_backslash(self) -> None:
        lines = [
            '10.0.0.1 - - [10/Nov/2026:17:10:00 +0000] "PUT /item HTTP/1.1" 201 15 "" "trail\\\\"',
            '10.0.0.1 - - [10/Nov/2026:17:10:01 +0000] "PATCH /item HTTP/1.1" 200 5 "" ""',
        ]
        report = self.analyzer.analyze(lines)
        self.assertEqual(report["total_requests"], 2)
        self.assertEqual(report["malformed_lines"], 0)
        self.assertEqual(report["methods"], {"PATCH": 1, "PUT": 1})

    def test_cli_valid_file_outputs_json_and_zero_exit(self) -> None:
        proc = self._run_cli(str(TESTS_DIR / "tc03_standard_mixed.log"))
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stderr, "")
        parsed = json.loads(proc.stdout)
        self.assertEqual(parsed["total_requests"], 6)
        self.assertEqual(parsed["total_bytes"], 5888)

    def test_cli_invalid_argument_counts_return_one(self) -> None:
        for argv in ((), ("a.log", "b.log")):
            proc = self._run_cli(*argv)
            self.assertEqual(proc.returncode, 1)
            self.assertEqual(proc.stdout, "")
            self.assertTrue(proc.stderr.strip())

    def test_cli_missing_file_and_directory_return_one(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            missing = Path(tmp_dir) / "does_not_exist.log"
            for target in (missing, tmp_dir):
                proc = self._run_cli(str(target))
                self.assertEqual(proc.returncode, 1)
                self.assertEqual(proc.stdout, "")
                self.assertTrue(proc.stderr.strip())


if __name__ == "__main__":
    unittest.main()
