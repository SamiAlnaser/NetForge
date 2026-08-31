import packet_capture


def test_build_tcpdump_command():
    command = packet_capture.build_tcpdump_command(
        interface="lo",
        output_file="reports/test.pcap",
        packet_filter="tcp port 8081",
        count=12,
    )

    assert command == [
        "tcpdump",
        "-i",
        "lo",
        "-nn",
        "-w",
        "reports/test.pcap",
        "-c",
        "12",
        "tcp port 8081",
    ]


def test_build_tcpdump_command_without_optional_arguments():
    command = packet_capture.build_tcpdump_command(
        interface="ens33",
        output_file="capture.pcap",
    )

    assert command == [
        "tcpdump",
        "-i",
        "ens33",
        "-nn",
        "-w",
        "capture.pcap",
    ]



def test_start_capture(monkeypatch):
    captured = {}

    class FakeProcess:
        pass

    def fake_popen(command, **kwargs):
        captured["command"] = command
        captured["kwargs"] = kwargs
        return FakeProcess()

    monkeypatch.setattr(
        packet_capture.subprocess,
        "Popen",
        fake_popen,
    )

    process = packet_capture.start_capture(
        interface="lo",
        output_file="reports/test.pcap",
        packet_filter="tcp port 8081",
        count=12,
    )

    assert isinstance(process, FakeProcess)
    assert captured["kwargs"]["start_new_session"] is True


def test_stop_capture(monkeypatch):
    events = []

    class FakeProcess:
        pid = 12345
        returncode = None

        def poll(self):
            return None

        def wait(self, timeout=None):
            events.append(("wait", timeout))
            return 0

    def fake_killpg(pid, sig):
        events.append(("killpg", pid, sig))

    monkeypatch.setattr(
        packet_capture.os,
        "killpg",
        fake_killpg,
    )

    process = FakeProcess()

    result = packet_capture.stop_capture(process)

    assert result == 0
    assert events == [
        ("killpg", 12345, packet_capture.signal.SIGINT),
        ("wait", 5),
    ]
