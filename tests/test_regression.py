from regression import (
    percentage_change,
    is_regression,
    evaluate_metric,
    summarize_regression,
)


def test_percentage_change():
    assert percentage_change(100, 120) == 20
    assert percentage_change(100, 90) == -10


def test_latency_regression():
    assert is_regression(100, 120, 10, True) is True
    assert is_regression(100, 105, 10, True) is False


def test_throughput_regression():
    assert is_regression(100, 80, 10, False) is True
    assert is_regression(100, 95, 10, False) is False


def test_evaluate_metric_fail():
    result = evaluate_metric(
        "http_p95",
        0.70,
        1.20,
        10,
        True
    )

    assert result["status"] == "FAIL"


def test_summarize_regression_pass():
    results = [
        {"metric": "http_p95", "status": "PASS"},
        {"metric": "ping_p95_ms", "status": "PASS"},
    ]

    summary = summarize_regression(results)

    assert summary["overall_status"] == "PASS"
    assert summary["failed_metrics"] == []


def test_summarize_regression_fail():
    results = [
        {"metric": "http_p95", "status": "FAIL"},
        {"metric": "ping_p95_ms", "status": "PASS"},
    ]

    summary = summarize_regression(results)

    assert summary["overall_status"] == "FAIL"
    assert summary["failed_metrics"] == ["http_p95"]


def test_compare_benchmark_detects_regression(tmp_path):
    import json
    from regression import compare_benchmark, summarize_regression

    baseline = {
        "http_p95": 0.70,
        "ping_p95_ms": 72.0,
        "throughput_mbps": 6500.0
    }

    current = {
        "http": {"p95": 1.20},
        "ping": {"p95_latency_ms": 72.0},
        "throughput": {"receiver_mbps": 6500.0}
    }

    thresholds = {
        "http_p95": 10,
        "ping_p95_ms": 15,
        "throughput_mbps": 10
    }

    baseline_file = tmp_path / "baseline.json"
    current_file = tmp_path / "current.json"
    thresholds_file = tmp_path / "thresholds.json"

    baseline_file.write_text(json.dumps(baseline))
    current_file.write_text(json.dumps(current))
    thresholds_file.write_text(json.dumps(thresholds))

    results = compare_benchmark(
        baseline_file,
        current_file,
        thresholds_file
    )

    summary = summarize_regression(results)

    assert summary["overall_status"] == "FAIL"
    assert summary["failed_metrics"] == ["http_p95"]
