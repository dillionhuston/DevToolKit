import socket
from concurrent.futures import ThreadPoolExecutor
import threading

def port_scan(host_port, start_port, end_port):
    print("scanning ")
    
    def scan_single_port(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host_port, port))
        sock.close()
        return port, result
    
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:  
        futures = [executor.submit(scan_single_port, port) for port in range(start_port, end_port + 1)]
        for future in futures:
            port, result = future.result()
            if result == 0:
                results.append((port, result))
    
    for port, result in sorted(results):
        print(f"sock open {port}")
        print(result)