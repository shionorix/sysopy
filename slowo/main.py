from zgadula import Guesser
import dict1
import dict2
import numpy
from connect import Connect
import linecache
from time import sleep

def pickServer():
    owners = ["Kuba", "Łukasz", "Zuzia", "Pati", "Georgij"]
    servers = open('servers.txt', 'r', encoding="UTF-8")
    for owner, line  in enumerate(servers):
        print(f"{owner+1}) {owners[owner]}: {line}")
    connectTo = int(input())
    server = linecache.getline("servers.txt", connectTo)
    return server.strip('\n').split(" ")

if __name__ == '__main__':
    serverCredentials = pickServer() # needs file servers.txt to connect where each line contains credentials in the following order: <ip> <port> <login> <password> 
    while True:
        connectedInstance = Connect(serverCredentials[0], int(serverCredentials[1]))
        authStatus = connectedInstance.auth(serverCredentials[2], serverCredentials[3])
        print(authStatus)
        if authStatus == 0:
            break
        alphabet = authStatus
        #print(f"Alphabet {alphabet}")
        encodedWord = connectedInstance.receive()
        # if int(encodedWord) < 100:
        #     encodedWord = connectedInstance.receive()
        #     encodedWord = connectedInstance.receive()
        print(f"Encoded word: {encodedWord}")
        guesser = Guesser(int(alphabet), encodedWord)
        guess = guesser.move()
        tries = 1
        while True:
            
            sentMessage = connectedInstance.send(f"{guess}\n")
            if not sentMessage:
                break

            response = connectedInstance.receive()
            if not response:
                break

            if response == '#':
                guess = guesser.move()
                continue
                
            elif response == '=' and guess[0] == '=':
                print(f"Word guessed in {tries} tries 🥳")
                points = connectedInstance.receive()
                print(f"Got {points} points 😎")

            elif response == '=' and guess[0] == '+':
                print(f"Letter \'{guess[2]}\' guessed 😺")
                positions = connectedInstance.receive()
                if len(positions) >= 5:
                    guesser.updateCandidates(guess[2], positions)
                    guess = guesser.move()
                else:
                    
                    print(f"Got {positions} points")

            elif response == '!' and guess[0] == '+':
                print(f"There is no \'{guess[2]}\' in word 😿")
                guesser.rejectCandidates(guess[2])
                guess = guesser.move()
            elif response == '!' and guess[0] == '=':
                print(f"\'{guess[:2]}\' not guessed 😿")
                guesser.wordlist = numpy.delete(guesser.wordlist, numpy.argwhere(guesser.wordlist == guess[:2]))
                guess = guesser.move()
            elif response[0] == '?':
                print("Ending game...\n-------------------------------------")
                break  
            else:
                print("Someone else guessed the word... 😡")
                break
            tries += 1
        del connectedInstance
        sleep(1.5)

            
            