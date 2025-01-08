import socket
import requests
from ipaddress import ip_network
from concurrent.futures import ThreadPoolExecutor

def scan_ip(ip, port, timeout):
    try:
        url = f"http://{ip}:{port}"
        response = requests.get(url, timeout=timeout)

        if "Not found your stream. PLease contact administrator to get correct stream name" in response.text:
            print(f"[FOUND] Motorola LPR detected at {ip}")
            return str(ip)
    except requests.RequestException:
        pass
    return None

def scan_ip_range(ip_range, port=8080, timeout=5, threads=1):
    print(f"[INFO] Starting scan on IP range: {ip_range}, Port: {port}, Threads: {threads}")

    network = ip_network(ip_range, strict=False)
    total_ips = len(list(network.hosts()))

    print(f"[INFO] Total IPs to scan: {total_ips}")

    found_devices = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_ip = {executor.submit(scan_ip, ip, port, timeout): ip for ip in network.hosts()}

        for idx, future in enumerate(future_to_ip):
            result = future.result()
            if result:
                found_devices.append(result)

            if idx % 10 == 0 or idx == total_ips - 1:
                print(f"[PROGRESS] Scanned {idx + 1}/{total_ips} IPs...")

    print(f"[INFO] Scan completed. Found {len(found_devices)} device(s).")

    if found_devices:
        with open("found_lpr_devices.txt", "w") as output_file:
            for device in found_devices:
                output_file.write(f"{device}\n")
        print(f"[INFO] Found devices saved to 'found_lpr_devices.txt'.")
    else:
        print("[INFO] No devices found.")

if __name__ == "__main__":
    ip_range = input("Enter IP range (e.g., 192.168.1.0/24): ").strip()
    threads = input("Enter number of threads (default 1): ").strip()

    try:
        threads = int(threads) if threads else 1
        scan_ip_range(ip_range, threads=threads)
    except ValueError as e:
        print(f"[ERROR] Invalid input: {e}")
