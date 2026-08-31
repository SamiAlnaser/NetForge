from unittest.mock import patch, MagicMock

from fault_injection import (
    run_tc,
    add_latency,
    add_packet_loss,
    limit_bandwidth,
    restore_network,
)


def test_run_tc():
    fake_result = MagicMock()

    with patch("fault_injection.subprocess.run", return_value=fake_result) as mock_run:
        result = run_tc(["qdisc", "show"])

        mock_run.assert_called_once_with(
            ["sudo", "tc", "qdisc", "show"],
            capture_output=True,
            text=True
        )

        assert result is fake_result


def test_add_latency():
    with patch("fault_injection.run_tc") as mock_run_tc:
        add_latency(100, "ens33")

        mock_run_tc.assert_called_once_with([
            "qdisc", "replace",
            "dev", "ens33",
            "root", "netem",
            "delay", "100ms"
        ])


def test_add_packet_loss():
    with patch("fault_injection.run_tc") as mock_run_tc:
        add_packet_loss(20, "ens33")

        mock_run_tc.assert_called_once_with([
            "qdisc", "replace",
            "dev", "ens33",
            "root", "netem",
            "loss", "20%"
        ])


def test_limit_bandwidth():
    with patch("fault_injection.run_tc") as mock_run_tc:
        limit_bandwidth(10, "ens33")

        mock_run_tc.assert_called_once_with([
            "qdisc", "replace",
            "dev", "ens33",
            "root", "netem",
            "rate", "10mbit"
        ])


def test_restore_network():
    with patch("fault_injection.run_tc") as mock_run_tc:
        restore_network("ens33")

        mock_run_tc.assert_called_once_with([
            "qdisc", "replace",
            "dev", "ens33",
            "root", "fq_codel"
        ])


def test_apply_latency_scenario():
    from fault_injection import apply_scenario

    with patch("fault_injection.add_latency") as mock:
        apply_scenario("latency", "ens33")
        mock.assert_called_once_with(100, "ens33")


def test_apply_packet_loss_scenario():
    from fault_injection import apply_scenario

    with patch("fault_injection.add_packet_loss") as mock:
        apply_scenario("packet-loss", "ens33")
        mock.assert_called_once_with(20, "ens33")


def test_apply_bandwidth_scenario():
    from fault_injection import apply_scenario

    with patch("fault_injection.limit_bandwidth") as mock:
        apply_scenario("bandwidth", "ens33")
        mock.assert_called_once_with(10, "ens33")


def test_unknown_scenario():
    import pytest
    from fault_injection import apply_scenario

    with pytest.raises(ValueError):
        apply_scenario("wrong")
