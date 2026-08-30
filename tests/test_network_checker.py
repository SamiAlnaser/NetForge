from unittest.mock import patch

from network_checker import (
    resolve_hostname,
    calculate_statistics,
    check_tcp_port,
)


def test_resolve_localhost():
    ip_address = resolve_hostname("localhost")

    assert ip_address is not None


def test_resolve_invalid_hostname():
    ip_address = resolve_hostname("netforge-does-not-exist.invalid")

    assert ip_address is None


def test_calculate_statistics():
    connection_times = [10, 20, 30]

    statistics = calculate_statistics(connection_times)

    assert statistics["average"] == 20
    assert statistics["minimum"] == 10
    assert statistics["maximum"] == 30


def test_calculate_statistics_empty_list():
    statistics = calculate_statistics([])

    assert statistics is None


def test_check_tcp_port_success():
    with patch("network_checker.socket.create_connection") as mock_connection:
        with patch(
            "network_checker.time.perf_counter",
            side_effect=[10.0, 10.05]
        ):
            reachable, connection_time = check_tcp_port(
                "127.0.0.1",
                443
            )

    assert reachable is True
    assert round(connection_time, 2) == 50.0

    mock_connection.assert_called_once_with(
        ("127.0.0.1", 443),
        timeout=3
    )


def test_check_tcp_port_failure():
    with patch(
        "network_checker.socket.create_connection",
        side_effect=OSError
    ):
        reachable, connection_time = check_tcp_port(
            "127.0.0.1",
            81
        )

    assert reachable is False
    assert connection_time is None
