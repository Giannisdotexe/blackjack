from random import randint
import time

def deck():
    deck = []
    for i in range(1, 5):
        for j in range(1, 14):
            deck.append((i, j))
    return deck


deck = deck()

def pick():
    dlen = len(deck) - 1
    rand = randint(0, dlen)
    drawncard = deck[rand]
    deck.remove(deck[rand])
    return drawncard

def dealerturn(total):
    while total <= 17:
        dealercard = pick()
        total += dealercard[1]
    return total, dealercard


def winner(p, d):
    if p > 21 and d > 21:
        print("You both bust")
    elif p > 21:
        print("You busted, You lost")
    elif d > 21:
        print("Dealer busted, You won")
    elif p > d:
        print("You won")
    elif p < d:
        print("You lost")
    elif p == d:
        print("Tie")

def value(total, aces):
    card = pick()
    value = card[1]
    if value > 10:
        value = 10
    if total + value > 21 and len(aces) > 0:  
        value -= 9
    if value == 1 and total + value <= 21:
        value = 11
    if value == 1 and total + value > 21:
        value = 1
    total += value
    return total, card


def initial():
    # dealer's inital cards
    dcards = []
    daces = []
    dealertotal = 0
    dealeroutput = value(dealertotal, daces)
    dealercard = dealeroutput[1]
    dealertotal = dealeroutput[0]
    dcards.append(dealercard)

    # player's inital cards
    pcards = []
    paces = []
    playertotal = 0
    for _ in range(2):
        playeroutput = value(playertotal, paces)
        playercard = playeroutput[1]
        playertotal = playeroutput[0]
        pcards.append(playercard)

    return dcards, dealertotal, daces, pcards, playertotal, paces


action = input("Stand or hit? ")
def turns(action):
    
    dcards, dealertotal, daces, pcards, playertotal, paces = initial()

    print("Dealer:")
    print(dcards, dealertotal)
    print("You:")
    print(pcards, playertotal)

    while playertotal <= 21:
        if action == 0: # 0 = hit
            output = value(playertotal, paces)
            playercard = output[1]
            if playercard[1] == 1:
                paces.append(playercard)
            playertotal = output[0]
            pcards.append(playercard)
            print("Dealer:")
            print(dcards, dealertotal)
            print("You:")
            print(pcards, playertotal)
        elif action == 1: # 1 = stand
            while dealertotal <= 17:
                output = value(dealertotal, daces)
                dealercard = output[1]
                if dealercard[1] == 1:
                    daces.append(dealercard)
                dealertotal = output[0]
                dcards.append(dealercard)
                print("Dealer:")
                print(dcards, dealertotal)
                print("You:")
                print(pcards, playertotal)
                time.sleep(1)
            break
    else:
        print("You busted")
        input()
        while dealertotal <= 17:
            output = value(dealertotal, daces)
            dealercard = output[1]
            if dealercard[1] == 1:
                daces.append(dealercard)
            dealertotal = output[0]
            dcards.append(dealercard)
            print("Dealer:")
            print(dcards, dealertotal)
            print("You:")
            print(pcards, playertotal)
            input()
    winner(playertotal, dealertotal)


# def pturn(action):
#     if action == 0: # 0 = hit
#         output = value(playertotal, paces)
#         playercard = output[1]
#         if playercard[1] == 1:
#             paces.append(playercard)
#         playertotal = output[0]
#         pcards.append(playercard)
#         print("Dealer:")
#         print(dcards, dealertotal)
#         print("You:")
#         print(pcards, playertotal)

if __name__ == "__main__":
    turns()