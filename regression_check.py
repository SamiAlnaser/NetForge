import sys
from regression import compare_benchmark, summarize_regression


DEFAULT_BASELINE = "baselines/baseline.json"
DEFAULT_CURRENT = "benchmark_result.json"
DEFAULT_THRESHOLDS = "config/regression_thresholds.json"


def main():
    current_file = (
        sys.argv[1]
        if len(sys.argv) > 1
        else DEFAULT_CURRENT
    )

    baseline_file = (
        sys.argv[2]
        if len(sys.argv) > 2
        else DEFAULT_BASELINE
    )

    thresholds_file = (
        sys.argv[3]
        if len(sys.argv) > 3
        else DEFAULT_THRESHOLDS
    )

    results = compare_benchmark(
        baseline_file,
        current_file,
        thresholds_file
    )

    summary = summarize_regression(results)

    print("\nNetForge Performance Regression Report")
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
        print("Regressions:", ", ".join(summary["failed_metrics"]))
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
