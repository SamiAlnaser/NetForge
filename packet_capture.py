import os
import signal
import subprocess


def build_tcpdump_command(
    interface,
    output_file,
    packet_filter=None,
    count=None
):
    command = [
        "tcpdump",
        "-i",
        interface,
        "-nn",
        "-w",
        str(output_file),
    ]

    if count is not None:
        command.extend(["-c", str(count)])

    if packet_filter:
        command.append(packet_filter)

    return command


def start_capture(
    interface,
    output_file,
    packet_filter=None,
    count=None
):
    command = build_tcpdump_command(
        interface=interface,
        output_file=output_file,
        packet_filter=packet_filter,
        count=count,
    )

    return subprocess.Popen(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )


def stop_capture(process, timeout=5):
    if process.poll() is not None:
        return process.returncode

    os.killpg(process.pid, signal.SIGINT)

    try:
        return process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        return process.wait()
