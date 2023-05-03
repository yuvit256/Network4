import socket
import io
import time


SERVER_ADDR = ("127.0.0.1", 8888)
NUM_CONNECTIONS = 300
BUFFER_SIZE = io.DEFAULT_BUFFER_SIZE
AUTH = f"{(8039) ^ (7214)}".encode()
TIMEOUT = 0.001
OK_MSG = b"Yuval&Ron"

def main():
    reno = []
    cubic = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(SERVER_ADDR)
        server.listen(NUM_CONNECTIONS)
        client, addr = server.accept()
        
        while True:
            start1 = time.time()
            with open("received_part1.txt", "wb") as file1:
                while True:
                    data = client.recv(BUFFER_SIZE)
                    if data.__contains__(OK_MSG):
                        break
                    file1.write(data)
            end1 = time.time()
            cubic.append(float(end1-start1))
            print(f"First file has been received")

            client.sendall(AUTH)
            time.sleep(TIMEOUT)
            print("Authentication has been sent.")

            client.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b"reno")
            print("Changing CC algorithem to reno.")

            start2 = time.time()
            with open("received_part2.txt", "wb") as file2:
                while True:
                    data = client.recv(BUFFER_SIZE)
                    if data.__contains__(OK_MSG):
                        break
                    file2.write(data)
            end2 = time.time()
            reno.append(float(end2-start2))
            print(f"Second file has been received")

            msg = client.recv(1024).decode()
            if msg == "again":
                continue
            elif msg == "bye":
                print("##############RESULTS##############")
                print("File-number      Cubic       Reno")
                cubic_total_time = 0
                reno_total_time = 0
                for i in range(len(cubic)): 
                    print(f"seq = {i} cubic = {cubic[i]} reno = {reno[i]}")
                    cubic_total_time = cubic_total_time + cubic[i]
                    reno_total_time = reno_total_time + reno[i]
                print(f"The avarge time for cubic is {cubic_total_time/len(cubic)}")
                print(f"The avarge time for reno is {reno_total_time/len(reno)}")
                client.close()
                break


if __name__ == "__main__":
    main()
