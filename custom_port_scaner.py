import socket
import threading
from queue import Queue

# ============================
# CONFIG
# ============================

NUM_THREADS = 200   # entre 100 y 400 va muy bien
PORT_RANGE = (1, 1024)

KNOWN_SERVICES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Proxy"
}

# ============================
# SCAN FUNCTION
# ============================

def scan_port(ip, port, results):
    try:
        s = socket.socket()
        s.settimeout(0.3)
        s.connect((ip, port))

        service = KNOWN_SERVICES.get(port, "Desconocido")
        banner = ""

        try:
            banner = s.recv(1024).decode(errors="ignore").strip()
        except:
            pass

        results.append((port, service, banner))

        s.close()

    except:
        pass


def worker(ip, queue, results):
    while not queue.empty():
        port = queue.get()
        scan_port(ip, port, results)
        queue.task_done()


# ============================
# MAIN
# ============================

def main():
    ip = input("IP objetivo: ")
    start_port, end_port = PORT_RANGE

    print(f"\nEscaneando {ip} desde el puerto {start_port} al {end_port}...\n")

    queue = Queue()
    results = []

    for port in range(start_port, end_port + 1):
        queue.put(port)

    for _ in range(NUM_THREADS):
        t = threading.Thread(target=worker, args=(ip, queue, results))
        t.daemon = True
        t.start()

    queue.join()

    # Ordenar resultados por puerto
    results.sort(key=lambda x: x[0])

    print("\n=========== RESULTADOS ===========")
    for port, service, banner in results:
        print(f"[+] Puerto {port} abierto ({service})")
        if banner:
            print(f"    Banner → {banner}")
    print("==================================\n")


if __name__ == "__main__":
    main()
