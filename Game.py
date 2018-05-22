import random
from Player import Player

class Cards:
    
    def __init__(self):
        self.deck = []
        for i in range(13):
            for _ in range(4):
                self.deck.append(i+1)
    
    def shuffle(self):
        random.shuffle(self.deck)
    
    def draw_top(self):
        return self.deck.pop();

class Game:
    
    def __init__(self):
        self.started = False
        self.players = []
        self.cards = Cards()
        self.cards.shuffle()
        self.stack = 0
        
    def new_player(self, player):
        self.players.append(player)
        
    def next_player(self):
        return self.players[0]
    
    def start_game(self):
        self.started = True
        for p in self.players:
            for _ in range(3):
                p.cards.append(self.cards.draw_top())
    
    def play(self, card, choice):
        reverse = False
        if card == 1:
            if choice == '+':
                self.stack += 11
            else:
                self.stack += 1
        if card == 4:
            reverse = True
            self.stack = self.stack
        if card == 9:
            self.stack = self.stack
        if card == 10:
            if choice == '+':
                self.stack += 10
            else:
                self.stack -= 10
        if card == 11 | card == 12:
            self.stack += 10
        if card == 13:
            self.stack = 99
        if stack > 99:
            return [stack, reverse, True]
        else:
            self.players[0].remove(card)
            self.players[0].append(self.deck.draw_top())
            current_player = self.players.pop(0)
            if reverse:
                self.players.reverse()
            self.players.append(current_player)
            return [stack, reverse, False]
        