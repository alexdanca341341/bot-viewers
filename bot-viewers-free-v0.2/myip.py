import requests
import socket

def get_my_ip():
    try:
        response = requests.get('http://ip.42.pl/raw')
        return response.text
    except requests.RequestException:
        return "Could not determine IP"

def check_protocol(protocol, host, port):
    try:
        sock = socket.create_connection((host, port), timeout=2)
        sock.close()
        print(f"Connection successful over {protocol} to {host}:{port}")
    except (socket.timeout, ConnectionRefusedError):
        print(f"Connection failed over {protocol} to {host}:{port}")

ip = get_my_ip()
print(f"My IP is: {ip}")

check_protocol("HTTP", "www.google.com", 80)
check_protocol("HTTPS", "www.google.com", 443)
