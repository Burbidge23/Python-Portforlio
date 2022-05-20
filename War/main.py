import war

game = war.Game()

names = []
for i in range(2):
        name = input("Enter the name of player " + str(i+1) + " ")
        names.append(name)

winner = game.play(names)

print(winner.name + " Has won the Game! Nice Win!")

