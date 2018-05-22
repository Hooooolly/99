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
        
    def new_player(self, name, number):
        self.players.append(Player(name, number))
    
    def start_game(self):
        self.started = True
        for p in self.players:
            for _ in range(3):
                p.cards.append(self.cards.draw_top())