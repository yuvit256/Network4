import signal
import sys
from socket import *
import os
import time
import struct


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
    seq = 0
    with socket(AF_INET, SOCK_RAW, IPPROTO_ICMP) as sock:
        while True:
            seq += 1
            ping = create_ping_packet()
            start = time.time()
            sock.sendto(ping, (sys.argv[1], 0))  # port 0 because of IP header
            pid = os.fork()
            if pid == 0:  # child
                os.execvp("python3", ["python3", "watchdog.py"])
            else:  # parent
                time.sleep(1)  # let watchdog start
                with socket(AF_INET, SOCK_STREAM, IPPROTO_TCP) as wd:
                    wd.connect(("127.0.0.1", 3000))
                    wd.sendall(sys.argv[1].encode())
                    pong = sock.recvfrom(8192)
                    end = time.time()
                    print(f"Packet IP: {pong[1][0]} , seq : #{seq} , time : {(end - start) - 1} seconds")
                    wd.shutdown(SHUT_RDWR)
                    os.kill(pid, signal.SIGTERM)
                    os.wait()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)