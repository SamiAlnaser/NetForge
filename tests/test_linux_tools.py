from types import SimpleNamespace

from linux_tools import parse_ping_result, parse_dig_result, parse_curl_result


def test_parse_ping_success():
    result = SimpleNamespace(
        returncode=0,
        stdout="""
4 packets transmitted, 4 received, 0% packet loss
rtt min/avg/max/mdev = 71.500/72.000/73.000/0.500 ms
""",
        stderr=""
    )

    parsed = parse_ping_result(result)

    assert parsed["reachable"] is True
    assert parsed["packet_loss_percent"] == 0.0
    assert parsed["minimum_ms"] == 71.5
    assert parsed["average_ms"] == 72.0
    assert parsed["maximum_ms"] == 73.0
    assert parsed["mdev_ms"] == 0.5
    assert parsed["error"] is None


def test_parse_ping_dns_failure():
    result = SimpleNamespace(
        returncode=2,
        stdout="",
        stderr="ping: bad.invalid: Name or service not known"
    )

    parsed = parse_ping_result(result)

    assert parsed["reachable"] is False
    assert parsed["packet_loss_percent"] is None
    assert parsed["average_ms"] is None
    assert parsed["error"] is not None


def test_parse_dig_success():
    result = SimpleNamespace(
        returncode=0,
        stdout="140.82.121.3\n",
        stderr=""
    )

    parsed = parse_dig_result(result)

    assert parsed["resolved"] is True
    assert parsed["return_code"] == 0
    assert parsed["answers"] == ["140.82.121.3"]
    assert parsed["error"] is None


def test_parse_dig_no_answer():
    result = SimpleNamespace(
        returncode=0,
        stdout="",
        stderr=""
    )

    parsed = parse_dig_result(result)

    assert parsed["resolved"] is False
    assert parsed["return_code"] == 0
    assert parsed["answers"] == []
    assert parsed["error"] is None


def test_parse_curl_success():
    result = SimpleNamespace(
        returncode=0,
        stdout="""http_code=200
dns=0.010000
tcp=0.080000
tls=0.180000
ttfb=0.320000
total=0.700000
""",
        stderr=""
    )

    parsed = parse_curl_result(result)

    assert parsed["success"] is True
    assert parsed["http_code"] == 200
    assert parsed["dns_seconds"] == 0.01
    assert parsed["tcp_seconds"] == 0.08
    assert parsed["tls_seconds"] == 0.18
    assert parsed["ttfb_seconds"] == 0.32
    assert parsed["total_seconds"] == 0.7
    assert parsed["error"] is None


def test_parse_curl_failure():
    result = SimpleNamespace(
        returncode=6,
        stdout="""http_code=000
dns=0.000000
tcp=0.000000
tls=0.000000
ttfb=0.000000
total=0.005000
""",
        stderr="curl: (6) Could not resolve host"
    )

    parsed = parse_curl_result(result)

    assert parsed["success"] is False
    assert parsed["return_code"] == 6
    assert parsed["http_code"] == 0
    assert parsed["total_seconds"] == 0.005
    assert parsed["error"] is not None
