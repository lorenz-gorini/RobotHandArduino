import socket

def main():
    host = "192.168.2.55"
    port = 23

    mySocket = socket.socket()
    mySocket.connect((host,port))

    message = input(" -> ")
    while True:
        mySocket.send(message.encode())
        data = mySocket.recv(200).decode()

        print(data)

if __name__ == "__main__":
    main()