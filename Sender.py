import os
import socket 

def main():
    fp = open('file.txt', 'rb') # Open the file in read mode
    file_size = os.path.getsize('file.txt') # tell the file size in bytes
    half_size = file_size//2
    first_half = fp.read(half_size)
    fp.seek(half_size)
    second_half = fp.read()
    fp1 = open('first_half.txt', 'wb') # Write the first half to a new file
    fp1.write(first_half)
    fp2 = open('second_half.txt', 'wb') # Write the second half to a new file
    fp2.write(second_half)

    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket
    receiver_addr = ('127.0.0.1', 8888)
    sender_socket.connect(receiver_addr) # connecting to the receiver
    sender_socket.sendall(first_half) # sending the first half of the file

    auth = sender_socket.recv(1024)
    print('auth = ', auth.decode())





if __name__ == "__main__":
    main()
