import socket
import sys
import threading

HOST = '127.0.0.1'
PORT = 6605   

if len(sys.argv) != 2:
    print("python client.py username")
    exit(0)

user = sys.argv[1]


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    s.send(str.encode(user))

    message = s.recv(1024).decode('utf-8')

    if(message[:1] == '#'):
        print('Username-ul este deja inregistrat!')
        s.close()
        exit(0)
    
    print(message)
    
    while True:
        message = s.recv(1024).decode('utf-8')

        if(message[:1] == 'J'):
            print(message)
            s.send(str.encode('received'))
        elif(message[:1] == 'A' or message[:1] == 'F'):
            print(message)
            s.close()
            break
        else:
            print(message)
            word = input()
            s.send(str.encode(word))