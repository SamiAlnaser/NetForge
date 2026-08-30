import pytest
from performance_metrics import percentile, calculate_metrics, calculate_ping_metrics


def test_percentile():
    values = [10, 20, 30, 40, 50]

    assert percentile(values, 50) == 30
    assert percentile(values, 95) == 50
    assert percentile(values, 99) == 50


def test_calculate_metrics():
    samples = [
        {"success": True, "total_seconds": 0.10},
        {"success": True, "total_seconds": 0.20},
        {"success": True, "total_seconds": 0.30},
        {"success": True, "total_seconds": 0.40},
        {"success": True, "total_seconds": 0.50},
    ]

    result = calculate_metrics(samples)

    assert result["runs"] == 5
    assert result["average"] == pytest.approx(0.30)
    assert result["minimum"] == 0.10
    assert result["maximum"] == 0.50
    assert result["p50"] == 0.30
    assert result["p95"] == 0.50
    assert result["p99"] == 0.50


def test_calculate_metrics_ignores_failed_samples():
    samples = [
        {"success": True, "total_seconds": 0.20},
        {"success": False, "total_seconds": 5.00},
        {"success": True, "total_seconds": 0.40},
    ]

    result = calculate_metrics(samples)

    assert result["runs"] == 2
    assert result["average"] == pytest.approx(0.30)


def test_calculate_metrics_no_successful_samples():
    samples = [
        {"success": False, "total_seconds": 1.00}
    ]

    assert calculate_metrics(samples) is None


def test_calculate_ping_metrics():
    samples = [
        {
            "reachable": True,
            "average_ms": 70.0,
            "packet_loss_percent": 0.0
        },
        {
            "reachable": True,
            "average_ms": 80.0,
            "packet_loss_percent": 0.0
        },
        {
            "reachable": True,
            "average_ms": 90.0,
            "packet_loss_percent": 5.0
        }
    ]

    result = calculate_ping_metrics(samples)

    assert result["runs"] == 3
    assert result["average_latency_ms"] == pytest.approx(80.0)
    assert result["minimum_latency_ms"] == 70.0
    assert result["maximum_latency_ms"] == 90.0
    assert result["p50_latency_ms"] == 80.0
    assert result["average_packet_loss_percent"] == pytest.approx(5 / 3)


def test_calculate_ping_metrics_no_reachable_samples():
    samples = [
        {
            "reachable": False,
            "average_ms": None,
            "packet_loss_percent": None
        }
    ]

    assert calculate_ping_metrics(samples) is None
