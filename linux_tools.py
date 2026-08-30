import subprocess


def run_ping(hostname, count=4):
    command = [
        "ping",
        "-c",
        str(count),
        hostname
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    return result


def parse_ping_result(result):
    import re

    data = {
        "reachable": result.returncode == 0,
        "return_code": result.returncode,
        "packet_loss_percent": None,
        "minimum_ms": None,
        "average_ms": None,
        "maximum_ms": None,
        "mdev_ms": None,
        "error": result.stderr.strip() or None
    }

    loss_match = re.search(
        r"([\d.]+)% packet loss",
        result.stdout
    )

    if loss_match:
        data["packet_loss_percent"] = float(loss_match.group(1))

    rtt_match = re.search(
        r"= ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+) ms",
        result.stdout
    )

    if rtt_match:
        data["minimum_ms"] = float(rtt_match.group(1))
        data["average_ms"] = float(rtt_match.group(2))
        data["maximum_ms"] = float(rtt_match.group(3))
        data["mdev_ms"] = float(rtt_match.group(4))

    return data


def run_dig(hostname, record_type="A"):
    command = [
        "dig",
        "+short",
        hostname,
        record_type
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    return result


def parse_dig_result(result):
    answers = [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    ]

    return {
        "resolved": result.returncode == 0 and len(answers) > 0,
        "return_code": result.returncode,
        "answers": answers,
        "error": result.stderr.strip() or None
    }


def run_curl(url):
    command = [
        "curl",
        "-sS",
        "-o",
        "/dev/null",
        "-w",
        "http_code=%{http_code}\n"
        "dns=%{time_namelookup}\n"
        "tcp=%{time_connect}\n"
        "tls=%{time_appconnect}\n"
        "ttfb=%{time_starttransfer}\n"
        "total=%{time_total}\n",
        url
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    return result


def parse_curl_result(result):
    values = {}

    for line in result.stdout.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            values[key] = value

    http_code = int(values.get("http_code", 0))

    return {
        "success": result.returncode == 0,
        "return_code": result.returncode,
        "http_code": http_code,
        "dns_seconds": float(values.get("dns", 0)),
        "tcp_seconds": float(values.get("tcp", 0)),
        "tls_seconds": float(values.get("tls", 0)),
        "ttfb_seconds": float(values.get("ttfb", 0)),
        "total_seconds": float(values.get("total", 0)),
        "error": result.stderr.strip() or None
    }
