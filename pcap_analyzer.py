
from scapy.all import rdpcap, IP, TCP, ICMP, Raw





def analyze_pcap(filename):

    packets = rdpcap(str(filename))



    summary = {

        "total_packets": len(packets),

        "ip_packets": 0,

        "tcp_packets": 0,

        "icmp_packets": 0,

        "syn_packets": 0,

        "syn_ack_packets": 0,

        "fin_packets": 0,

        "http_requests": 0,

        "http_responses": 0,

    }



    for packet in packets:

        if IP in packet:

            summary["ip_packets"] += 1



        if ICMP in packet:

            summary["icmp_packets"] += 1



        if TCP in packet:

            summary["tcp_packets"] += 1



            flags = int(packet[TCP].flags)



            if flags & 0x02 and flags & 0x10:

                summary["syn_ack_packets"] += 1

            elif flags & 0x02:

                summary["syn_packets"] += 1



            if flags & 0x01:

                summary["fin_packets"] += 1



        if Raw in packet:

            payload = bytes(packet[Raw].load)

            if payload.startswith(b"GET "):
                summary["http_requests"] += 1

            if payload.startswith(b"HTTP/"):
                summary["http_responses"] += 1

    return summary
