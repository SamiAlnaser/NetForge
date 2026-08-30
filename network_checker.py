import socket





def resolve_hostname(hostname):

    try:

        ip_address = socket.gethostbyname(hostname)

        return ip_address



    except socket.gaierror:

        return None





hostname = input("Enter hostname: ")



ip_address = resolve_hostname(hostname)



if ip_address:

    print("Hostname:", hostname)

    print("IP Address:", ip_address)

else:

    print("DNS resolution failed for:", hostname)
