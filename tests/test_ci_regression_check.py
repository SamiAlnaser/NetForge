import json

from ci_regression_check import compare_ci_reports
from regression import summarize_regression


def write_json(path, data):
    path.write_text(json.dumps(data))


def make_report(http_p95, ping_p95, throughput):
    return {
        "http": {
            "p95": http_p95
        },
        "ping": {
            "p95_latency_ms": ping_p95
        },
        "throughput": {
            "receiver_mbps": throughput
        }
    }


def test_compare_ci_reports_passes(tmp_path):
    baseline = make_report(
        0.0020,
        0.060,
        10000
    )

    current = make_report(
        0.0021,
        0.062,
        9500
    )

    thresholds = {
        "http_p95": 10,
        "ping_p95_ms": 10,
        "throughput_mbps": 10
    }

    baseline_file = tmp_path / "baseline.json"
    current_file = tmp_path / "current.json"
    thresholds_file = tmp_path / "thresholds.json"

    write_json(baseline_file, baseline)
    write_json(current_file, current)
    write_json(thresholds_file, thresholds)

    results = compare_ci_reports(
        baseline_file,
        current_file,
        thresholds_file
    )

    summary = summarize_regression(results)

    assert summary["overall_status"] == "PASS"
    assert summary["failed_metrics"] == []


def test_compare_ci_reports_detects_http_regression(tmp_path):
    baseline = make_report(
        0.0020,
        0.060,
        10000
    )

    current = make_report(
        0.0030,
        0.060,
        10000
    )

    thresholds = {
        "http_p95": 20,
        "ping_p95_ms": 20,
        "throughput_mbps": 20
    }

    baseline_file = tmp_path / "baseline.json"
    current_file = tmp_path / "current.json"
    thresholds_file = tmp_path / "thresholds.json"

    write_json(baseline_file, baseline)
    write_json(current_file, current)
    write_json(thresholds_file, thresholds)

    results = compare_ci_reports(
        baseline_file,
        current_file,
        thresholds_file
    )

    summary = summarize_regression(results)

    assert summary["overall_status"] == "FAIL"
    assert summary["failed_metrics"] == ["http_p95"]


def test_compare_ci_reports_detects_throughput_regression(tmp_path):
    baseline = make_report(
        0.0020,
        0.060,
        10000
    )

    current = make_report(
        0.0020,
        0.060,
        7000
    )

    thresholds = {
        "http_p95": 20,
        "ping_p95_ms": 20,
        "throughput_mbps": 20
    }

    baseline_file = tmp_path / "baseline.json"
    current_file = tmp_path / "current.json"
    thresholds_file = tmp_path / "thresholds.json"

    write_json(baseline_file, baseline)
    write_json(current_file, current)
    write_json(thresholds_file, thresholds)

    results = compare_ci_reports(
        baseline_file,
        current_file,
        thresholds_file
    )

    summary = summarize_regression(results)

    assert summary["overall_status"] == "FAIL"
    assert summary["failed_metrics"] == ["throughput_mbps"]
