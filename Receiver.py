from socket import *

serverPort = 8888
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('127.0.0.1',serverPort))
serverSocket.listen(1)
print ('The server is ready to receive\n')
while True:
    connectionSocket, addr = serverSocket.accept()
    # start timer
    with open('received.txt', 'wb') as file:
        data = connectionSocket.recv(1024)
        while data:
            file.write(data)
            data = connectionSocket.recv(1024)
    # end timer
    print ('The first half of the file received\n')

    yuval_id = 8039
    ron_id = 7214
    xor = str(yuval_id ^ ron_id)
    connectionSocket.send(xor.encode())

    connectionSocket.close()