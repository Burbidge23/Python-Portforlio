import cards


class Hand(object):

    def __init__(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def give(self, other_hand, card):
        self.cards.remove(card)
        other_hand.add(card)

    def clear(self):
        self.cards.clear()

    def __str__(self):
        rep = ""
        if self.cards:
            for card in self.cards:
                rep += str(card)
        else:
            rep = "<EMPTY!>"

        return rep


class Deck(Hand):

    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def deal(self, players, amount=1):
        cards_needed = len(players) * amount
        if len(self.cards) >= cards_needed:
            for i in range(amount):
                for player in players:
                    top_card = self.cards[0]
                    self.give(player, self.cards[0])
        else:
            print("Out of Cards")
            for player in players:
                player.clear()
            self.clear()
            self.populate()
            self.shuffle()
            self.deal(players, amount)

    def populate(self):
        for rank in cards.Card.RANKS:
            for suit in cards.Card.SUITS:
                card = cards.Pos_Card(rank, suit)
                self.add(card)

if __name__ == "__main__":
    print("this is a module not a script try running the main")
    input("\n\nPress the enter key to exit.")