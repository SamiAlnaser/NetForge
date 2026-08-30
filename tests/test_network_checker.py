from network_checker import resolve_hostname, calculate_statistics


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
