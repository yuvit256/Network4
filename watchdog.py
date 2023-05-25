import time
import socket

SERVER_ADDR = ('127.0.0.1', 3000)
NUM_CONNECTIONS = 300
BUFFER_SIZE = io.DEFAULT_BUFFER_SIZE # 8192

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(SERVER_ADDR)
        server.listen(NUM_CONNECTIONS)
        client, addr = server.accept()
        start = time.time()
        i=1
        while msg = server.recv(BUFFER_SIZE) == None : 
            time.sleep(1)
            i=i+1
            if i == 10:
                print(f"server {msg.decode()} cannot be reached")
        end = time.time()
                
        
if __name__ == "__main__":
    main()