from collections import namedtuple
from random import randint
import requests
import socket
import sys
import SocketServer
import re




board = namedtuple("board", "field1 field2 field3 field4")
pPos = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
pMon = [500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
b1 = board(0, 0, "Road", 50)  # initialing struct and 20 element long array ownedby, upgrade, name, cost
myBoard = [b1] * 16  # 16 lines long


def sendData(data):
    HOST, PORT = "137.154.224.245", 4628
    var = 0
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))

        sock.sendall(str(data[0]) + "," + str(data[1]) + "," + str(data[2]) + "\n")
        for x in myBoard:
            sock.sendall(str(x[0]) + "," + str(x[1]) + "," + str(x[3]) + "\n")
            sock.sendall(str(x[2]) + "\n")


        # Receive data from the server and shut down
        received = sock.recv(1024)
    finally:
        sock.close()

    print "Sent:     {}".format(data)
    print "Received: {}".format(received)


def send_request():
    # Request
    # POST https://api.transport.nsw.gov.au/v1/ttds/route

    try:
        response = requests.post(
            url="https://api.transport.nsw.gov.au/v1/ttds/route",
            headers={
                "Accept": "application/vnd.ttds-route+json",
                "Authorization": "apikey l7xx38c1c031e2974386bbecebc6bf64885b",
                "Content-Type": "application/vnd.ttds-route+json",
                "User-Agent": "Anthony/1.0",
            },
            data="{\"encoded-paths\": [\"|lolE}qiy[btCxtAzrAzKxz@a{@p}AgxB\"],\"departure-time\": 1695168000}"
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def roll():
    diceroll = randint(0, 6) + randint(0, 6)  # roll d6 twice
    print "You rolled: " , diceroll
    return diceroll

def options():
    print "XXXXXXXXXXXXXX TOLLS XXXXXXXXXXXXXX"
    print "0 Roll Dice and Move!"
    print "1 Buy Road!"
    print "2 Trade Player"
    print "3 Sell Road"
    print "4 Upgrade Road"
    print "5 End Turn"
    print "6 Concede"
    print "7 Print Board"
    print "XXXXXXXXXXXXXX TOLLS XXXXXXXXXXXXXX\n\n"
    return  int(raw_input())

#y = amount to move, x = playerID
def movePlayer(x,y):
    pPos[x] = (pPos[x] + y)%20
    return

def upgrade(x):
    return

def buyRoad(x):
    if pMon[x] - myBoard[pPos[x]][3] < 0:
        pMon[x] = pMon[x] - myBoard[pPos[x]][3]
        myBoard[pPos[x]][0] = x
        print "Congratulations, you bought: ",myBoard[pPos[x]][2]
    else:
        print "Not Enough Money!"


def decide( x , y ):
    if x == 0:            #Roll Dice and move
        movePlayer(y,roll())
        return
    elif x == 1:          #Buy Road underneath player
        return 0
    elif x == 2:          #Trade
        return 0
    elif x == 3:          #Sell Property
        return 0
    elif x == 4:          #Upgrade
        return 0
    elif x == 5:          #End Turn
        return -999
    elif x == 6:          #Concede
        return 6
    elif x == 7:          #Concede
        printBoard(y)
        return

def printBoard(pCount):
    print "XXXXXXXXXXXXX"
    print "X", myBoard[8][0], myBoard[9][0], myBoard[10][0], myBoard[11][0], myBoard[12][0], "X"
    print "X", myBoard[7][0], "X", "X", "X", myBoard[13][0], "X"
    print "X", myBoard[6][0], "X", "X", "X", myBoard[14][0], "X"
    print "X", myBoard[5][0], "X", "X", "X", myBoard[15][0], "X"
    print "X", myBoard[4][0], myBoard[3][0], myBoard[2][0], myBoard[1][0], myBoard[1][0], "X"
    print "XXXXXXXXXXXXX\n"
    print "Player ID: ", pCount
    print "Money: ", pMon[pCount]
    return

def compressData(x):
    compress = namedtuple("compress", "field1 field2 field3")
    c1 = compress(x, pPos[x], pMon[x])
    sendData(c1)


class main:
    win = 0;

    print "How many players will there be?"
    y = raw_input()
    y = int(y)

    z = 0
    for x in pPos:              #sets amount of players by looping through array
        if ( y < 1):
            pPos[z] = -999
        y=y-1
        z=z+1

    var = 0
    while (win==0):              #while no winner
        pCount = 0;
        for x in pPos:           #for every player
            printBoard(pCount)
            if x != -999:       #if player hasn't lost
                while var != -999:
                    var = options()
                    #compressData(pCount)
                    if (decide(var, pCount) == 6):
                        win = 1;
                        print "Player" , x+1 , "Wins"
            pCount = pCount + 1