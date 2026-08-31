import subprocess


DEFAULT_INTERFACE = "ens33"


def run_tc(arguments):
    command = ["sudo", "tc"] + arguments

    return subprocess.run(
        command,
        capture_output=True,
        text=True
    )


def add_latency(delay_ms=100, interface=DEFAULT_INTERFACE):
    return run_tc([
        "qdisc", "replace",
        "dev", interface,
        "root", "netem",
        "delay", f"{delay_ms}ms"
    ])


def add_packet_loss(loss_percent=20, interface=DEFAULT_INTERFACE):
    return run_tc([
        "qdisc", "replace",
        "dev", interface,
        "root", "netem",
        "loss", f"{loss_percent}%"
    ])


def limit_bandwidth(rate_mbit=10, interface=DEFAULT_INTERFACE):
    return run_tc([
        "qdisc", "replace",
        "dev", interface,
        "root", "netem",
        "rate", f"{rate_mbit}mbit"
    ])


def restore_network(interface=DEFAULT_INTERFACE):
    return run_tc([
        "qdisc", "replace",
        "dev", interface,
        "root", "fq_codel"
    ])


def apply_scenario(name, interface=DEFAULT_INTERFACE):
    scenarios = {
        "latency": lambda: add_latency(100, interface),
        "packet-loss": lambda: add_packet_loss(20, interface),
        "bandwidth": lambda: limit_bandwidth(10, interface),
    }

    if name not in scenarios:
        raise ValueError(
            f"Unknown scenario: {name}. "
            f"Available: {', '.join(scenarios)}"
        )

    return scenarios[name]()
