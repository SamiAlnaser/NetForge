import json
import sys

from regression import evaluate_metric, summarize_regression


def load_json(filename):
    with open(filename, "r") as file:
        return json.load(file)


def compare_ci_reports(
    baseline_filename,
    current_filename,
    thresholds_filename
):
    baseline = load_json(baseline_filename)
    current = load_json(current_filename)
    thresholds = load_json(thresholds_filename)

    return [
        evaluate_metric(
            "http_p95",
            baseline["http"]["p95"],
            current["http"]["p95"],
            thresholds["http_p95"],
            True
        ),
        evaluate_metric(
            "ping_p95_ms",
            baseline["ping"]["p95_latency_ms"],
            current["ping"]["p95_latency_ms"],
            thresholds["ping_p95_ms"],
            True
        ),
        evaluate_metric(
            "throughput_mbps",
            baseline["throughput"]["receiver_mbps"],
            current["throughput"]["receiver_mbps"],
            thresholds["throughput_mbps"],
            False
        )
    ]


def main():
    if len(sys.argv) != 4:
        print(
            "Usage: python ci_regression_check.py "
            "<baseline_report> <current_report> <thresholds>"
        )
        return 2

    baseline_file = sys.argv[1]
    current_file = sys.argv[2]
    thresholds_file = sys.argv[3]

    results = compare_ci_reports(
        baseline_file,
        current_file,
        thresholds_file
    )

    summary = summarize_regression(results)

    print("\nNetForge Relative Performance Report")
    print("=" * 42)

    for result in summary["results"]:
        change = result["change_percent"]

        if change is not None:
            change = round(change, 2)

        print(
            f'{result["metric"]}: '
            f'baseline={result["baseline"]}, '
            f'current={result["current"]}, '
            f'change={change}%, '
            f'threshold={result["threshold_percent"]}% '
            f'-> {result["status"]}'
        )

    print("=" * 42)
    print("Overall:", summary["overall_status"])

    if summary["overall_status"] == "FAIL":
        print(
            "Regressions:",
            ", ".join(summary["failed_metrics"])
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
