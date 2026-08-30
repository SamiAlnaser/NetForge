from linux_tools import run_curl, parse_curl_result


def collect_http_samples(url, runs=5):
    samples = []

    for _ in range(runs):
        result = run_curl(url)
        parsed = parse_curl_result(result)
        samples.append(parsed)

    return samples


def calculate_metrics(samples, metric="total_seconds"):
    values = [
        sample[metric]
        for sample in samples
        if sample["success"]
    ]

    if not values:
        return None

    values.sort()

    return {
        "runs": len(values),
        "average": sum(values) / len(values),
        "minimum": min(values),
        "maximum": max(values)
    }


def percentile(values, percent):
    if not values:
        return None

    values = sorted(values)

    import math

    index = math.ceil((percent / 100) * len(values)) - 1
    return values[index]


def percentile(values, percent):
    if not values:
        return None

    import math

    values = sorted(values)
    index = math.ceil((percent / 100) * len(values)) - 1

    return values[index]


def calculate_metrics(samples, metric="total_seconds"):
    values = [
        sample[metric]
        for sample in samples
        if sample["success"]
    ]

    if not values:
        return None

    values.sort()

    return {
        "runs": len(values),
        "average": sum(values) / len(values),
        "minimum": min(values),
        "maximum": max(values),
        "p50": percentile(values, 50),
        "p95": percentile(values, 95),
        "p99": percentile(values, 99)
    }


from linux_tools import run_ping, parse_ping_result


def collect_ping_samples(hostname, runs=5, count=4):
    samples = []

    for _ in range(runs):
        result = run_ping(hostname, count)
        parsed = parse_ping_result(result)
        samples.append(parsed)

    return samples


def calculate_ping_metrics(samples):
    latencies = [
        sample["average_ms"]
        for sample in samples
        if sample["reachable"] and sample["average_ms"] is not None
    ]

    losses = [
        sample["packet_loss_percent"]
        for sample in samples
        if sample["packet_loss_percent"] is not None
    ]

    if not latencies:
        return None

    return {
        "runs": len(latencies),
        "average_latency_ms": sum(latencies) / len(latencies),
        "minimum_latency_ms": min(latencies),
        "maximum_latency_ms": max(latencies),
        "p50_latency_ms": percentile(latencies, 50),
        "p95_latency_ms": percentile(latencies, 95),
        "p99_latency_ms": percentile(latencies, 99),
        "average_packet_loss_percent": (
            sum(losses) / len(losses) if losses else None
        )
    }
