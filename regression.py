import json


def percentage_change(baseline, current):
    if baseline == 0:
        return None

    return ((current - baseline) / baseline) * 100


def is_regression(
    baseline,
    current,
    threshold_percent,
    lower_is_better=True
):
    change = percentage_change(baseline, current)

    if change is None:
        return False

    if lower_is_better:
        return change > threshold_percent

    return change < -threshold_percent


def evaluate_metric(
    name,
    baseline,
    current,
    threshold_percent,
    lower_is_better=True
):
    change = percentage_change(baseline, current)

    regression = is_regression(
        baseline,
        current,
        threshold_percent,
        lower_is_better
    )

    return {
        "metric": name,
        "baseline": baseline,
        "current": current,
        "change_percent": change,
        "threshold_percent": threshold_percent,
        "lower_is_better": lower_is_better,
        "status": "FAIL" if regression else "PASS"
    }


def load_baseline(filename):
    with open(filename, "r") as file:
        return json.load(file)


def load_thresholds(filename):
    with open(filename, "r") as file:
        return json.load(file)


def compare_benchmark(
    baseline_filename,
    current_filename,
    thresholds_filename
):
    baseline = load_baseline(baseline_filename)
    thresholds = load_thresholds(thresholds_filename)

    with open(current_filename, "r") as file:
        current = json.load(file)

    return [
        evaluate_metric(
            "http_p95",
            baseline["http_p95"],
            current["http"]["p95"],
            thresholds["http_p95"],
            True
        ),
        evaluate_metric(
            "ping_p95_ms",
            baseline["ping_p95_ms"],
            current["ping"]["p95_latency_ms"],
            thresholds["ping_p95_ms"],
            True
        ),
        evaluate_metric(
            "throughput_mbps",
            baseline["throughput_mbps"],
            current["throughput"]["receiver_mbps"],
            thresholds["throughput_mbps"],
            False
        )
    ]


def summarize_regression(results):
    failed = [
        result["metric"]
        for result in results
        if result["status"] == "FAIL"
    ]

    return {
        "overall_status": "FAIL" if failed else "PASS",
        "total_metrics": len(results),
        "failed_metrics": failed,
        "results": results
    }
