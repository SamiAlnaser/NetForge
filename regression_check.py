import sys
from regression import compare_benchmark, summarize_regression


BASELINE = "baselines/baseline.json"
DEFAULT_CURRENT = "benchmark_result.json"
THRESHOLDS = "config/regression_thresholds.json"


def main():
    current_file = (
        sys.argv[1]
        if len(sys.argv) > 1
        else DEFAULT_CURRENT
    )

    results = compare_benchmark(
        BASELINE,
        current_file,
        THRESHOLDS
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
