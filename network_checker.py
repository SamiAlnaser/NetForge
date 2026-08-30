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

        if connection_times:
            average_time = sum(connection_times) / len(connection_times)
            minimum_time = min(connection_times)
            maximum_time = max(connection_times)

            print("TCP Port", port, "is reachable")
            print("Average connection time:", round(average_time, 2), "ms")
            print("Minimum connection time:", round(minimum_time, 2), "ms")
            print("Maximum connection time:", round(maximum_time, 2), "ms")

        else:
            print("TCP Port", port, "is not reachable")

    else:
        print("DNS resolution failed for:", hostname)


if __name__ == "__main__":
    main()
