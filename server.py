import socket
import sys

HOST = 'sys.ase.ro'                
PORT = 6605

if len(sys.argv) != 2:
    print('python server.py number_of_players')
    exit(0)

number_of_players = int(sys.argv[1])

print('Fazan\nproiect realizat de Bișag Alexandru Ștefan în cadrul disciplinei Rețele de Calculatoare')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(10)

    msg = ''
    connections = []
    usernames = []
    words = []
    nr = 0

    print('Serverul de joc a fost pornit!')

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
                msg = "Jocul a început!"
            elif nr == number_of_players-1:
                msg = "Jocul va începe în curând. Mai este nevoie de un jucător."
            else:
                msg = "Jocul va începe în curând. Mai este nevoie de " + str(number_of_players - nr) + " jucători"

            conn.send(msg.encode())
            print(username + " s-a alaturat jocului.")

    while nr > 1:
        for i in range(0, nr):
            if words:
                lastLetters = words[len(words)-1][-2::]
                msg = 'Introdu un cuvânt care să înceapă cu literele: ' + lastLetters
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
                    print('Jucătorul ' + usernames[i] + ' a fost eliminat!')    
                    usernames.remove(usernames[i])
                    connections[i].close()
                    connections.remove(connections[i])
                    words = []
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
    connections[0].close()

    s.close()