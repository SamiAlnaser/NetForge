import json

import benchmark_runner as br


def test_save_benchmark(tmp_path):
    report = {
        "http": {"average": 0.5},
        "ping": {"average_latency_ms": 70.0}
    }

    filename = tmp_path / "benchmark.json"

    result = br.save_benchmark(report, str(filename))

    assert result == str(filename)

    saved = json.loads(filename.read_text())

    assert saved == report


def test_run_benchmark(monkeypatch):
    monkeypatch.setattr(
        br,
        "collect_http_samples",
        lambda url, runs: [{"success": True, "total_seconds": 0.5}]
    )

    monkeypatch.setattr(
        br,
        "collect_ping_samples",
        lambda hostname, runs, count: [{
            "reachable": True,
            "average_ms": 70.0,
            "packet_loss_percent": 0.0
        }]
    )

    monkeypatch.setattr(
        br,
        "run_iperf3",
        lambda server, duration: object()
    )

    monkeypatch.setattr(
        br,
        "parse_iperf3_result",
        lambda result: {
            "success": True,
            "sender_mbps": 6000.0,
            "receiver_mbps": 5990.0,
            "retransmits": 0
        }
    )

    report = br.run_benchmark(
        "https://example.com",
        "example.com",
        "192.168.88.1"
    )

    assert report["targets"]["url"] == "https://example.com"
    assert report["http"]["average"] == 0.5
    assert report["ping"]["average_latency_ms"] == 70.0
    assert report["throughput"]["receiver_mbps"] == 5990.0
