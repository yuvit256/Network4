import os
import signal
import time
from socket import *


try:
    with socket(AF_INET, SOCK_STREAM, IPPROTO_TCP) as sock:
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", 3000))
        sock.listen(5)
        client, addr = sock.accept()
        ip = client.recv(8192)
        for i in range(10):
            time.sleep(1)
        client.shutdown(SHUT_RDWR)
    print(f"server {ip.decode()} cannot be reached")
    os.kill(os.getppid(), signal.SIGTERM)
except KeyboardInterrupt:
    pass

