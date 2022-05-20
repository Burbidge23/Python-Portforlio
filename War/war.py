import cards
import hands

class War_Card(cards.Pos_Card):
    # Add Comment
    @property
    def value(self):
        v = None
        if self.facingUp:
            v = War_Card.RANKS.index(self.rank) + 1
            if v == 1:
                v = 14
        return v

class War_Deck(hands.Deck):
    # Add Comment
    def populate(self):
        for rank in cards.Card.RANKS:
            for suit in cards.Card.SUITS:
                card = War_Card(rank, suit)
                self.add(card)

class War_Hand(hands.Hand):
    # Add Comment
    def __init__(self, name):
        super(War_Hand, self).__init__()
        self.name = name
    def give_three(self, other_hand):
        if len(self.cards) >= 3:
            for i in range(3):
                self.give(other_hand, self.cards[0])
        else:
            self.clear()

    def shuffle(self):
        import random
        random.shuffle(self.cards)


class War_Pot(War_Hand):
    # Add Comment
    def give_all(self, winner, player1, player2, pot, players):
        if winner == player1:
            for i in range(len(self.cards)):
                x = self.cards[0]
                self.give(winner, x)
        elif winner == player2:
            for i in range(len(self.cards)):
                x = self.cards[0]
                self.give(winner, x)
        else:
            for player in players:
                player.give_three(pot)

class War_Table(hands.Hand):
    # Add Comment
    def pick_winner(self,players, pot):
        if self.cards[0].value == self.cards[1].value:
            winner = pot
        elif self.cards[0].value > self.cards[1].value:
            winner = players[0]
        else:
            winner = players[1]
        for i in range(len(self.cards)):
            x = self.cards[0]
            self.give(pot, x)

        return winner

class Game(object):
    def play(self, names):
        player1 = War_Hand(names[0])
        player2 = War_Hand(names[1])
        players = [player1, player2]
        deck = War_Deck()
        deck.populate()
        deck.shuffle()
        deck.deal(players, 26)
        table = War_Table()
        pot = War_Pot("War")
        turn = 0
        playing = True

        while playing:
            player1.give(table, player1.cards[0])
            player2.give(table, player2.cards[0])
            print(table)
            winner = table.pick_winner(players, pot)
            print(winner.name+" wins")
            pot.give_all(winner, players[0], players[1], pot, players)
            print(player1.name+": " + str(len(player1.cards)))
            print(player2.name+": " + str(len(player2.cards)))
            turn += 1
            print("turn:"+str(turn))
            input('press enter to continue')

            if len(player1.cards) == 0:
                playing = False
                return player2
            elif len(player2.cards) == 0:
                playing = False
                return player1

            if turn%100 == 0:
                player1.shuffle()
                player2.shuffle()



