import socket
import time
import json


def resolve_hostname(hostname):
    try:
        return socket.gethostbyname(hostname)

    except socket.gaierror:
        return None


def check_tcp_port(ip_address, port):
    try:
        start_time = time.perf_counter()

        with socket.create_connection((ip_address, port), timeout=3):
            end_time = time.perf_counter()

        connection_time = (end_time - start_time) * 1000

        return True, connection_time

    except OSError:
        return False, None


def measure_tcp_connections(ip_address, port, attempts=5):
    connection_times = []

    for attempt in range(attempts):
        reachable, connection_time = check_tcp_port(ip_address, port)

        if reachable:
            connection_times.append(connection_time)

            print(
                "Attempt",
                attempt + 1,
                "- Connection time:",
                round(connection_time, 2),
                "ms"
            )

        else:
            print(
                "Attempt",
                attempt + 1,
                "- TCP connection failed"
            )

    return connection_times


def calculate_statistics(connection_times):
    if not connection_times:
        return None

    return {
        "average": sum(connection_times) / len(connection_times),
        "minimum": min(connection_times),
        "maximum": max(connection_times)
    }


def run_network_check(hostname, port, attempts=5):
    ip_address = resolve_hostname(hostname)

    if not ip_address:
        return {
            "hostname": hostname,
            "ip_address": None,
            "port": port,
            "reachable": False,
            "attempts": attempts,
            "average_ms": None,
            "minimum_ms": None,
            "maximum_ms": None
        }

    connection_times = measure_tcp_connections(
        ip_address,
        port,
        attempts
    )

    statistics = calculate_statistics(connection_times)

    if not statistics:
        return {
            "hostname": hostname,
            "ip_address": ip_address,
            "port": port,
            "reachable": False,
            "attempts": attempts,
            "average_ms": None,
            "minimum_ms": None,
            "maximum_ms": None
        }

    return {
        "hostname": hostname,
        "ip_address": ip_address,
        "port": port,
        "reachable": True,
        "attempts": attempts,
        "average_ms": statistics["average"],
        "minimum_ms": statistics["minimum"],
        "maximum_ms": statistics["maximum"]
    }


def save_result_to_json(result, filename="network_result.json"):
    with open(filename, "w") as file:
        json.dump(result, file, indent=4)


def main():
    hostname = input("Enter hostname: ")
    port = int(input("Enter TCP port: "))

    result = run_network_check(hostname, port)

    print()
    print("NetForge Network Check")
    print("----------------------")
    print("Hostname:", result["hostname"])
    print("IP Address:", result["ip_address"])
    print("TCP Port:", result["port"])
    print("Reachable:", result["reachable"])

    if result["reachable"]:
        print("Average connection time:", round(result["average_ms"], 2), "ms")
        print("Minimum connection time:", round(result["minimum_ms"], 2), "ms")
        print("Maximum connection time:", round(result["maximum_ms"], 2), "ms")

    save_result_to_json(result)

    print()
    print("Result saved to network_result.json")

def is_within_threshold(average_ms, threshold_ms):
    if average_ms is None:
        return False

    return average_ms <= threshold_ms

if __name__ == "__main__":
    main()
