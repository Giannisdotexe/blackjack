from random import randint
import time
import sys
import pygame
import pygame.time
from button import Button
import player
from state import State

pygame.init()
screen = pygame.display.set_mode((1200,800))
screen.fill((0, 120, 0))

logo = pygame.image.load("assets/logo32x32.png").convert_alpha()
img = pygame.image.load("assets/cropstart.png").convert()
font = pygame.font.SysFont('Consolas', 20)
pygame.display.set_icon(logo)
pygame.display.set_caption("Play Blackjack")
clock = pygame.time.Clock()

# for player in connected_players:
#   player1 = player.Player(player.id, player.name, player.balance) 
#   players.append(player1)
#   something like that

gamer = player.Player(1, "John", 5000)

cardWidth = 71
cardLength = 96
x = 600 - cardWidth
pcardY = 600
dcardY = 100
cardsprite = pygame.sprite.Sprite() # possible idea
cropped = pygame.Surface((cardWidth, cardLength))
areatotal = pygame.Surface((cardWidth, 20), pygame.SRCALPHA) # pygame.SRCALPHA for transparent colors RGBA values
balarea = pygame.Surface((100, 50), pygame.SRCALPHA)
balarea.fill((0, 0, 0, 0))
secarea = pygame.Surface((25, 20))
secarea.fill((0, 0, 0))
amountarea = pygame.Surface((100, 30))
# btnsurf = pygame.Surface((100, 170), pygame.SRCALPHA)
# btnsurf.fill((0, 0, 0, 0))
running = True
done = False

bet_event = pygame.USEREVENT + 1
stand_event = pygame.USEREVENT + 2
timer_event = pygame.USEREVENT + 3

def deck():
    deck = []
    for i in range(1, 5): # 1, 5?
        for j in range(1, 14): #1, 14?
            deck.append((i, j))
    return deck

class Blackjack:
    def __init__(self):
        self.deck = deck()

        self.dcards = []
        self.daces = []
        self.dealertotal = 0

        self.pcards = []
        self.paces = []
        self.playertotal = 0

        self.dtotaltext = font.render(str(self.dealertotal), True, (0, 0, 0))
        self.ptotaltext = font.render(str(self.playertotal), True, (0, 0, 0))
        
        self.balance = gamer.balance
        self.bet_amount = 0

        #self.bet_event = pygame.USEREVENT + 1
        #self.stand_event = pygame.USEREVENT + 2
        #self.timer = pygame.USEREVENT + 3
        self.seconds = 10

    def pick(self):
        dlen = len(self.deck) - 1
        rand = randint(0, dlen)
        drawncard = self.deck[rand]
        self.deck.remove(self.deck[rand])
        return drawncard

    def winner(self):
        p = self.playertotal
        d = self.dealertotal
        if p > 21 and d > 21:
            print("You both bust")
            self.balance += self.bet_amount
        elif p > 21:
            print("You busted, You lost")
        elif d > 21:
            print("Dealer busted, You won")
            self.balance += self.bet_amount * 2
        elif p > d:
            print("You won")
            self.balance += self.bet_amount * 2
        elif p < d:
            print("You lost")
        elif p == d:
            print("Tie")
            self.balance += self.bet_amount
        else:
            print(p, d)
            print("wtf?")
        gamer.balance = self.balance
        balarea.fill((0, 120, 0))
        bal = font.render(str(self.balance), True, (0, 0, 0))
        balarea.blit(bal, (0, 0))
        screen.blit(balarea, (1000, 400))

    def value(self, total, aces):
        card = self.pick()
        value = card[1]
        if value > 10:
            value = 10
        if value == 1:
            aces.append(card)
            value = 11
        if total + value > 21 and len(aces) > 0:
            value -= 10
            aces.pop(0) # I guess suit doesn't matter for now?
        # if value == 1 and total + value <= 21:
        #     value = 11
        # if value == 1 and total + value > 21:
        #     value = 1
        total += value
        return total, card

    def place(self, c, x, y):
        left = (2*(c[1]-1)) + (71*(c[1]-1))
        top = (2*(c[0]-1)) + (96*(c[0]-1))

        reg = (left, top, cardWidth, cardLength)
        crop = img.subsurface(reg)

        # #region = (left, top, left + cardWidth, top + cardLength)
        # cropped.blit(img, (0, 0), region)
        
        screen.blit(crop, (x, y))
        
    def wait(self, ms):
        pass

    # animate everything in order
    # maybe use some sort of decorator to display dealer's cards in between
    def initial(self):
        balarea.fill((0, 120, 0))
        bal = font.render(str(self.balance), True, (0, 0, 0))
        balarea.blit(bal, (0, 0))
        screen.blit(balarea, (1000, 400))
        # dealer's inital cards
        dealeroutput = self.value(self.dealertotal, self.daces)
        dealercard = dealeroutput[1]
        self.dealertotal = dealeroutput[0]
        self.dcards.append(dealercard)
        self.place(dealercard, x + (len(self.dcards) - 1), dcardY)
        # display the dealer total
        areatotal.fill((0, 120, 0))
        self.dtotaltext = font.render(str(self.dealertotal), True, (0, 0, 0))
        areatotal.blit(self.dtotaltext, self.dtotaltext.get_rect(center = areatotal.get_rect().center))
        screen.blit(areatotal, (x, 200))

        pygame.display.update()
        pygame.time.delay(1000)

        

        # player's inital cards
        for _ in range(2):
            playeroutput = self.value(self.playertotal, self.paces)
            playercard = playeroutput[1]
            self.playertotal = playeroutput[0]
            self.pcards.append(playercard)
            self.place(playercard, x + (len(self.pcards) - 1) * 15, pcardY)
            # display the player total
            areatotal.fill((0, 120, 0)) # instead of making it the same color as the background, find a way to make it transparent
            self.ptotaltext = font.render(str(self.playertotal), True, (0, 0, 0))
            areatotal.blit(self.ptotaltext, self.ptotaltext.get_rect(center = areatotal.get_rect().center))
            screen.blit(areatotal, (x, 575))

            pygame.display.update()
            pygame.time.delay(1000)
        
        return True

    def reset(self):
        self.dcards = []
        self.daces = []
        self.dealertotal = 0

        self.pcards = []
        self.paces = []
        self.playertotal = 0

        self.bet_amount = 0

        self.seconds = 10


    def dturn(self):
        while self.dealertotal <= 17:
            output = self.value(self.dealertotal, self.daces)
            dealercard = output[1]
            self.dealertotal = output[0]
            self.dcards.append(dealercard)
            self.place(dealercard, x + (len(self.dcards) - 1) * 15, dcardY)

            areatotal.fill((0, 120, 0))
            self.dtotaltext = font.render(str(self.dealertotal), True, (0, 0, 0))
            areatotal.blit(self.dtotaltext, self.dtotaltext.get_rect(center = areatotal.get_rect().center))
            screen.blit(areatotal, (x, 200))

            pygame.display.update()
            pygame.time.delay(1000)
        self.winner()

        return True
        # self.replay()
        # running = False

    def hit(self):
        output = self.value(self.playertotal, self.paces)
        playercard = output[1]
        self.playertotal = output[0]
        self.pcards.append(playercard)
        self.place(playercard, x + (len(self.pcards) - 1) * 15, pcardY)

        areatotal.fill((0, 120, 0))
        self.ptotaltext = font.render(str(self.playertotal), True, (0, 0, 0))
        areatotal.blit(self.ptotaltext, self.ptotaltext.get_rect(center = areatotal.get_rect().center))
        screen.blit(areatotal, (x, 575))

        pygame.display.update()
        pygame.time.delay(100)
        
        pygame.time.set_timer(stand_event, 10000)
        pygame.time.set_timer(timer_event, 1000)
        self.reset_timer()
        

    def pturn(self):
        # timer_text = font.render("10", True, (0, 0, 0))
        # screen.blit(timer_text, (100, 500))
        doublebtn = Button(screen, 100, 50, "Double Down", (0, 0, 128), (100, 100), (255, 255, 255), 15, 15)
        hitbtn = Button(screen, 100, 50, "Hit", (128, 0, 0), (100, 160), radius=15)
        standbtn = Button(screen, 100, 50, "Stand", (0, 0, 128), (100, 220), (255, 255, 255), radius=15)
        pygame.display.update()
        if doublebtn.click():
            self.balance -= self.bet_amount
            self.bet_amount *= 2
            amountarea.fill((0, 120, 0))
            str_amount = font.render(str(self.bet_amount), True, (0, 0, 0))
            amountarea.blit(str_amount, str_amount.get_rect(center = amountarea.get_rect().center))
            screen.blit(amountarea, (200, 450))
            self.hit()
        if hitbtn.click():
            self.hit()
        if standbtn.click() or self.playertotal >= 21:
            # pygame.time.set_timer(stand_event, 0)
            # pygame.time.set_timer(countdown, 0)
            return self.dturn()
        # if pygame.event.get(countdown):
        #     if seconds > 0:
        #         seconds -= 1
        #         timer_text = font.render(str(seconds), True, (0, 0, 0))
        #         screen.blit(timer_text, (100, 500))
        #     else:
        #         pygame.time.set_timer(countdown, 0)
    # dont know where to put this
    def bet(self):
        amount = int()
        did_not_bet = False
        finishbtn = Button(screen, 100, 50, "Done", (0, 0, 128), (200, 490), (255, 255, 255), radius=15)
        tenbtn = Button(screen, 100, 50, "10", (128, 0, 0), (200, 550), radius=15)
        fiftybtn = Button(screen, 100, 50, "50", (0, 0, 128), (200, 610), (255, 255, 255), radius=15)
        hundbtn = Button(screen, 100, 50, "100", (128, 0, 0), (200, 670), radius=15)
        fivebtn = Button(screen, 100, 50, "500", (0, 0, 128), (200, 730), (255, 255, 255), radius=15)
        if tenbtn.click():
            amount = 10
            pygame.time.delay(200)
        elif fiftybtn.click():
            amount = 50
            pygame.time.delay(200)
        elif hundbtn.click():
            amount = 100
            pygame.time.delay(200)
        elif fivebtn.click():
            amount = 500
            pygame.time.delay(200)
        elif finishbtn.click():
            pygame.event.post(pygame.event.Event(bet_event))
        else:
            did_not_bet = True
            return # should I return?

        if self.balance - amount >= 0:
            self.balance -= amount
        else:
            amount = self.balance
            self.balance = 0
        self.bet_amount += amount


        amountarea.fill((0, 120, 0))
        str_amount = font.render(str(self.bet_amount), True, (0, 0, 0))
        amountarea.blit(str_amount, str_amount.get_rect(center = amountarea.get_rect().center))
        screen.blit(amountarea, (200, 450))

        # self.bet_amount += amount
        return did_not_bet

    def turns(self):
        self.bet(100)
        self.initial()
        self.pturn2()
        replaybtn = None # replay button

    def clear_timer(self):
        secarea.fill((0, 120, 0))
        sectext = font.render(str(self.seconds), True, (0, 0, 0))
        secarea.blit(sectext, (0, 0))
        screen.blit(secarea, (400, 400))

    def count(self):
        self.seconds -= 1
        self.clear_timer()

    def reset_timer(self):
        self.seconds = 10
        self.clear_timer()
    


def initialize():
    screen.fill((0, 120, 0))
    bj = Blackjack()
    did_bet = False
    did_bet = bj.bet()
    if did_bet:
        bj.initial()
    return bj


bj = Blackjack()

def mainloop():
    # bj = initialize()
    screen.fill((0, 120, 0))
    pygame.display.flip()
    state = State()
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == bet_event:
                pygame.time.set_timer(bet_event, 0)
                pygame.time.set_timer(timer_event, 0)
                secarea.fill((0, 120, 0))
                screen.blit(secarea, (400, 400))
                state.init = bj.initial()
                state.can_bet = False
                # has_bet = False
                bj.reset_timer()
            if event.type == stand_event:
                state.game_over = bj.dturn()
            if event.type == timer_event:
                bj.count()
        if not state.bet:
            pygame.time.set_timer(bet_event, 10000)
            pygame.time.set_timer(timer_event, 1000)
            state.bet = True
        if state.can_bet:
            bj.bet()
        # print(clock.get_time())
        if not state.game_over and state.init:
            if not state.stand:
                pygame.time.set_timer(stand_event, 10000)
                pygame.time.set_timer(timer_event, 1000)
                state.stand = True
            state.game_over = bj.pturn() 
        if state.game_over:
            pygame.time.set_timer(stand_event, 0)
            pygame.time.set_timer(timer_event, 0)
            secarea.fill((0, 120, 0))
            screen.blit(secarea, (400, 400))
            replaybtn = Button(screen, 200, 200, "Play Again", (128, 0, 0), (500, 300))
            nobtn = Button(screen, 200, 50, "No", (128, 0, 200), (500, 510))
            if replaybtn.click():
                # running = True
                bj.reset()
                mainloop()
            if nobtn.click():
                pygame.quit()
                sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    mainloop()

# play = True
# replay
# def replay():
#     global running
#     replaybtn = Button(screen, 200, 200, "Play Again?", (128, 0, 0), (600, 600))
#     pygame.display.update()
#     end_event = pygame.USEREVENT + 3
#     pygame.time.set_timer(end_event, 10000)
#     for event in pygame.event.get():
#         if event.type == end_event:
#             pygame.quit()
#             sys.exit()
#     if replaybtn.click():
#         running = True
#         mainloop()

# while play:
# mainloop()
# replay()