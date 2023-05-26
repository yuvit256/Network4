import time
import socket
import io

SERVER_ADDR = ("127.0.0.1", 3000)
NUM_CONNECTIONS = 300
BUFFER_SIZE = io.DEFAULT_BUFFER_SIZE # 8192

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(SERVER_ADDR)
        server.listen(NUM_CONNECTIONS)
        client, addr = server.accept()
        msg = client.recv(BUFFER_SIZE)
        print(f"IP = {msg.decode()}")
        client.close()
        
if __name__ == "__main__":
    main()