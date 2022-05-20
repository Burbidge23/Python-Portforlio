import random


class Card(object):
    RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    SUITS = ["♡", "♠", "♣", "♢"]

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __pick_rank_suit__():
        rank = random.choice(Card.RANKS)
        suit = random.choice(Card.SUITS)
        return rank, suit

    def __str__(self):
        rep = str.format("""
        ===========
        | {0}{1}       |
        |          |
        |          |
        |          |
        |          |
        |       {0}{1}|
        ===========
        """, self.rank, self.suit)
        return rep


class Pos_Card(Card):

    def __init__(self, rank, suit):
        super(Pos_Card, self).__init__(rank, suit)
        self.facingUp = True

    def flip(self):
        self.facingUp = not self.facingUp

    def __str__(self):
        if self.facingUp:
            rep = super(Pos_Card, self).__str__()

        else:
            rep = """
            ===========
            |          |
            |          |
            |          |
            |          |
            |          |
            |          |
            ===========
        """
        return rep

if __name__ == "__main__":
    print("this is a module not a script try running the main")
    input("\n\nPress the enter key to exit.")