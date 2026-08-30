import socket
import time


def resolve_hostname(hostname):
    try:
        ip_address = socket.gethostbyname(hostname)
        return ip_address

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

    statistics = {
        "average": sum(connection_times) / len(connection_times),
        "minimum": min(connection_times),
        "maximum": max(connection_times)
    }

    return statistics


def main():
    hostname = input("Enter hostname: ")
    port = int(input("Enter TCP port: "))

    ip_address = resolve_hostname(hostname)

    if ip_address:
        print("Hostname:", hostname)
        print("IP Address:", ip_address)

        connection_times = measure_tcp_connections(
            ip_address,
            port
        )

        statistics = calculate_statistics(connection_times)

        if statistics:
            print("TCP Port", port, "is reachable")
            print(
                "Average connection time:",
                round(statistics["average"], 2),
                "ms"
            )
            print(
                "Minimum connection time:",
                round(statistics["minimum"], 2),
                "ms"
            )
            print(
                "Maximum connection time:",
                round(statistics["maximum"], 2),
                "ms"
            )

        else:
            print("TCP Port", port, "is not reachable")

    else:
        print("DNS resolution failed for:", hostname)


if __name__ == "__main__":
    main()
