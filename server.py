import socket
import sys

HOST = 'localhost'                
PORT = 6605

if len(sys.argv) != 2:
    print('python server.py number_of_players')
    exit(0)

number_of_players = int(sys.argv[1])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(10)

    message = ''
    connections = []
    notifiers = []
    usernames = []
    words = []
    nr = 0

    print('server started')
    ##generate random first letter server-side
    ##multiple servers for multiple games in the same time
    ##user can create or join a game
    ##if he creates, a token will be generated and others cand join using this token
    ##use classes
    #create functions
    #extract constants

    while nr < number_of_players:
        conn, addr = s.accept()

        username = conn.recv(1024).decode("utf-8")

        if username in usernames:
            conn.send('#'.encode())
        else:
            connections.append(conn)
            usernames.append(username)
            nr = len(connections)

            if nr == number_of_players:
                msg = "Jocul a inceput!"
            elif nr == number_of_players -1:
                msg = "Jocul va incepe in curand. Mai este nevoie de un jucator."
            else:
                msg = "Jocul va incepe in curand. Mai este nevoie de " + str(number_of_players - nr) + " jucatori"

            conn.send(msg.encode())

            print(username + " s-a alaturat jocului.")

    while nr > 1:
        for i in range(0, nr):
            if words:
                lastLetters = words[len(words)-1][-2::]
                msg = 'Introdu un cuvant care sa inceapa cu literele: ' + lastLetters
                connections[i].send(msg.encode())
                word = connections[i].recv(1024).decode('utf-8')
                current_username = usernames[i]

                if word[:2] == lastLetters:
                    words.append(word)

                    for j in range(0, nr):
                        msg = 'Jucatorul ' + current_username + ' a spus cuvantul ' + word
                        connections[j].send(msg.encode())
                        connections[j].recv(1024)
                else:

                    for j in range(0, nr):
                        msg = 'Jucatorul ' + current_username + ' a spus cuvantul ' + word + ' si a fost eliminat!'
                        connections[j].send(msg.encode())
                        connections[j].recv(1024)

                    connections[i].send('Ai fost eliminat!'.encode())
                    usernames.remove(usernames[i])
                    connections.remove(connections[i])
                    break
            else:
                msg = 'Esti primul. Introdu un cuvant: '
                connections[i].send(msg.encode())
                word = connections[i].recv(1024).decode('utf-8')
                words.append(word)
                current_username = usernames[i]
                for j in range(0, nr):
                    msg = 'Jucatorul ' + current_username + ' a spus cuvantul ' + word
                    connections[j].send(msg.encode())
                    connections[j].recv(1024)

        nr = len(usernames)

    print('Castigatorul jocului este ' + usernames[0])
    connections[0].send('Felicitari! Ai castigat!'.encode())
    
s.close()