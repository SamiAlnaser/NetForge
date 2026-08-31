import pytest

import ci_benchmark


def make_report(http_p95, ping_p95, throughput, packet_loss=0.0):
    return {
        "http": {
            "p95": http_p95
        },
        "ping": {
            "p95_latency_ms": ping_p95,
            "average_packet_loss_percent": packet_loss
        },
        "throughput": {
            "success": True,
            "receiver_mbps": throughput
        }
    }


def test_run_ci_benchmark_uses_median(monkeypatch):
    reports = iter([
        make_report(0.003, 0.070, 9000),
        make_report(0.001, 0.050, 27000),
        make_report(0.002, 0.060, 10000),
    ])

    monkeypatch.setattr(
        ci_benchmark,
        "run_benchmark",
        lambda *args, **kwargs: next(reports)
    )

    result = ci_benchmark.run_ci_benchmark(
        "http://web:8080",
        "server",
        "server",
        repetitions=3
    )

    assert result["repetitions"] == 3
    assert result["http"]["p95"] == 0.002
    assert result["ping"]["p95_latency_ms"] == 0.060
    assert result["throughput"]["receiver_mbps"] == 10000

    assert result["http"]["samples"] == [
        0.003,
        0.001,
        0.002
    ]

    assert result["throughput"]["samples"] == [
        9000,
        27000,
        10000
    ]


def test_run_ci_benchmark_rejects_zero_repetitions():
    with pytest.raises(
        ValueError,
        match="repetitions must be at least 1"
    ):
        ci_benchmark.run_ci_benchmark(
            "http://web:8080",
            "server",
            "server",
            repetitions=0
        )


def test_run_ci_benchmark_fails_on_throughput_error(monkeypatch):
    report = make_report(0.002, 0.060, 0)
    report["throughput"]["success"] = False

    monkeypatch.setattr(
        ci_benchmark,
        "run_benchmark",
        lambda *args, **kwargs: report
    )

    with pytest.raises(
        RuntimeError,
        match="Throughput benchmark failed"
    ):
        ci_benchmark.run_ci_benchmark(
            "http://web:8080",
            "server",
            "server",
            repetitions=1
        )
