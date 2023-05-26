import socket
import sys
import time
import os
import io
import signal
import struct

WD_ADDR = ("127.0.0.1", 3000)
BUFFER_SIZE = io.DEFAULT_BUFFER_SIZE # 8192

def calculate_checksum(data):
    checksum = 0
    # Handle odd-length case
    if len(data) % 2 != 0:
        data += b'\x00'
    # Iterate over 16-bit chunks
    for i in range(0, len(data), 2):
        chunk = data[i:i+2]
        word = struct.unpack('!H', chunk)[0]
        checksum += word
    # Add carry bits
    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum += checksum >> 16
    # One's complement
    checksum = ~checksum & 0xFFFF
    return checksum

def create_ping_packet():
    icmp_type = 8  # ICMP Echo Request
    icmp_code = 0
    icmp_checksum = 0
    icmp_identifier = 12345
    icmp_sequence = 1
    # Construct ICMP header
    icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_identifier, icmp_sequence)
    # Calculate checksum
    icmp_checksum = calculate_checksum(icmp_header)
    # Update ICMP header with checksum
    icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_identifier, icmp_sequence)
    # Construct complete ICMP packet
    icmp_packet = icmp_header
    return icmp_packet

def main():
    try: 
        ping_pkt = create_ping_packet()
        with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as sock:
            seq = 0
            while True:
                start = time.time()
                sock.sendto(ping_pkt, (sys.argv[1], 8)) 
                pid = os.fork()
                if pid == 0:
                    os.execvp("python3", ["python3", "watchdog.py"])
                time.sleep(0.01)
                sockWD = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
                sockWD.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sockWD.connect(WD_ADDR)
                pong_pkt = sock.recvfrom(BUFFER_SIZE)
                sockWD.sendall((pong_pkt[1][0]).encode())
                end = time.time()
                time.sleep(0.5)
                print(f"Packet IP: {pong_pkt[1][0]} , seq : #{seq} , time : {end-start} seconds")
                seq = seq + 1
            sockWD.close()
    except KeyboardInterrupt: 
        if sock:
            sock.close()


if __name__ == "__main__":
    main()
