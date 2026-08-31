from reporting import build_markdown_report


def test_build_markdown_report():
    summary = {
        "overall_status": "PASS",
        "results": [
            {
                "metric": "http_p95",
                "baseline": 0.10,
                "current": 0.11,
                "change_percent": 10.0,
                "threshold_percent": 20,
                "status": "PASS"
            }
        ]
    }

    report = build_markdown_report(summary)

    assert "# NetForge Performance Report" in report
    assert "**Overall Status:** PASS" in report
    assert "| http_p95 | 0.1 | 0.11 | +10.00% | 20% | PASS |" in report


def test_write_markdown_report(tmp_path):
    from ci_regression_check import write_markdown_report

    summary = {
        "overall_status": "PASS",
        "results": [
            {
                "metric": "throughput_mbps",
                "baseline": 10000,
                "current": 9500,
                "change_percent": -5.0,
                "threshold_percent": 10,
                "status": "PASS"
            }
        ]
    }

    output_file = tmp_path / "performance-report.md"

    report = write_markdown_report(summary, output_file)

    assert output_file.exists()
    assert output_file.read_text() == report
    assert "# NetForge Performance Report" in report
    assert "| throughput_mbps | 10000 | 9500 | -5.00% | 10% | PASS |" in report
