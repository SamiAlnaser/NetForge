import argparse
import json
from datetime import datetime, timezone
from statistics import median

from benchmark_runner import run_benchmark


def run_ci_benchmark(
    url,
    hostname,
    iperf_server,
    repetitions=3
):
    if repetitions < 1:
        raise ValueError("repetitions must be at least 1")

    runs = []

    for _ in range(repetitions):
        report = run_benchmark(
            url,
            hostname,
            iperf_server
        )
        runs.append(report)

    http_p95 = []
    ping_p95 = []
    throughput = []
    packet_loss = []

    for report in runs:
        if report["http"] is None:
            raise RuntimeError("HTTP benchmark failed")

        if report["ping"] is None:
            raise RuntimeError("Ping benchmark failed")

        if not report["throughput"]["success"]:
            raise RuntimeError("Throughput benchmark failed")

        http_p95.append(report["http"]["p95"])
        ping_p95.append(report["ping"]["p95_latency_ms"])
        packet_loss.append(
            report["ping"]["average_packet_loss_percent"]
        )
        throughput.append(
            report["throughput"]["receiver_mbps"]
        )

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "repetitions": repetitions,
        "targets": {
            "url": url,
            "hostname": hostname,
            "iperf_server": iperf_server
        },
        "http": {
            "p95": median(http_p95),
            "samples": http_p95
        },
        "ping": {
            "p95_latency_ms": median(ping_p95),
            "average_packet_loss_percent": median(packet_loss),
            "samples": ping_p95
        },
        "throughput": {
            "success": True,
            "receiver_mbps": median(throughput),
            "samples": throughput
        },
        "raw_runs": runs
    }


def main():
    parser = argparse.ArgumentParser(
        description="Run repeated NetForge CI benchmarks"
    )

    parser.add_argument(
        "--url",
        default="http://web:8080"
    )

    parser.add_argument(
        "--hostname",
        default="server"
    )

    parser.add_argument(
        "--iperf-server",
        default="server"
    )

    parser.add_argument(
        "--repetitions",
        type=int,
        default=3
    )

    parser.add_argument(
        "--output",
        default="reports/docker-benchmark.json"
    )

    args = parser.parse_args()

    report = run_ci_benchmark(
        args.url,
        args.hostname,
        args.iperf_server,
        args.repetitions
    )

    with open(args.output, "w") as file:
        json.dump(report, file, indent=4)

    print("NetForge CI benchmark completed")
    print("Repetitions:", report["repetitions"])
    print("HTTP p95 median:", report["http"]["p95"])
    print("Ping p95 median:", report["ping"]["p95_latency_ms"])
    print(
        "Throughput median:",
        report["throughput"]["receiver_mbps"],
        "Mbps"
    )


if __name__ == "__main__":
    main()
