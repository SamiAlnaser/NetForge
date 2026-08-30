from datetime import datetime, timezone

from linux_tools import run_iperf3, parse_iperf3_result
from performance_metrics import (
    collect_http_samples,
    calculate_metrics,
    collect_ping_samples,
    calculate_ping_metrics,
)


def run_benchmark(
    url,
    hostname,
    iperf_server,
    http_runs=5,
    ping_runs=5,
    ping_count=4,
    iperf_duration=5
):
    http_samples = collect_http_samples(url, http_runs)
    ping_samples = collect_ping_samples(hostname, ping_runs, ping_count)

    iperf_result = run_iperf3(iperf_server, iperf_duration)
    throughput = parse_iperf3_result(iperf_result)

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "targets": {
            "url": url,
            "hostname": hostname,
            "iperf_server": iperf_server
        },
        "http": calculate_metrics(http_samples),
        "ping": calculate_ping_metrics(ping_samples),
        "throughput": throughput
    }


def save_benchmark(report, filename="benchmark_result.json"):
    import json

    with open(filename, "w") as file:
        json.dump(report, file, indent=4)

    return filename
