from scapy.all import IP, TCP, ICMP, Raw, wrpcap

from pcap_analyzer import analyze_pcap


def test_analyze_tcp_http_capture(tmp_path):
    packets = [
        IP(src="10.0.0.1", dst="10.0.0.2") /
        TCP(sport=50000, dport=8081, flags="S"),

        IP(src="10.0.0.2", dst="10.0.0.1") /
        TCP(sport=8081, dport=50000, flags="SA"),

        IP(src="10.0.0.1", dst="10.0.0.2") /
        TCP(sport=50000, dport=8081, flags="PA") /
        Raw(load=b"GET / HTTP/1.1\r\nHost: test\r\n\r\n"),

        IP(src="10.0.0.2", dst="10.0.0.1") /
        TCP(sport=8081, dport=50000, flags="PA") /
        Raw(load=b"HTTP/1.1 200 OK\r\n\r\n"),

        IP(src="10.0.0.1", dst="10.0.0.2") /
        TCP(sport=50000, dport=8081, flags="FA"),

        IP(src="10.0.0.2", dst="10.0.0.1") /
        TCP(sport=8081, dport=50000, flags="FA"),
    ]

    capture = tmp_path / "http.pcap"
    wrpcap(str(capture), packets)

    summary = analyze_pcap(capture)

    assert summary["total_packets"] == 6
    assert summary["ip_packets"] == 6
    assert summary["tcp_packets"] == 6
    assert summary["icmp_packets"] == 0
    assert summary["syn_packets"] == 1
    assert summary["syn_ack_packets"] == 1
    assert summary["fin_packets"] == 2
    assert summary["http_requests"] == 1
    assert summary["http_responses"] == 1


def test_analyze_icmp_capture(tmp_path):
    capture = tmp_path / "icmp.pcap"

    wrpcap(
        str(capture),
        [IP(src="10.0.0.1", dst="10.0.0.2") / ICMP()]
    )

    summary = analyze_pcap(capture)

    assert summary["total_packets"] == 1
    assert summary["ip_packets"] == 1
    assert summary["tcp_packets"] == 0
    assert summary["icmp_packets"] == 1


def test_cli_text_output(tmp_path, monkeypatch, capsys):
    from pcap_analyzer import main

    capture = tmp_path / "cli.pcap"

    wrpcap(
        str(capture),
        [IP(src="10.0.0.1", dst="10.0.0.2") / ICMP()]
    )

    monkeypatch.setattr(
        "sys.argv",
        ["pcap_analyzer.py", str(capture)]
    )

    main()

    output = capsys.readouterr().out

    assert "NetForge PCAP Analysis" in output
    assert "total_packets: 1" in output
    assert "icmp_packets: 1" in output


def test_cli_json_output(tmp_path, monkeypatch, capsys):
    import json
    from pcap_analyzer import main

    capture = tmp_path / "cli-json.pcap"

    wrpcap(
        str(capture),
        [IP(src="10.0.0.1", dst="10.0.0.2") / ICMP()]
    )

    monkeypatch.setattr(
        "sys.argv",
        ["pcap_analyzer.py", str(capture), "--json"]
    )

    main()

    output = capsys.readouterr().out
    data = json.loads(output)

    assert data["total_packets"] == 1
    assert data["icmp_packets"] == 1
