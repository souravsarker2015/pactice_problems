import random, itertools

deck = list(itertools.product(range(1, 14), ['heart', 'dimond', 'spead', 'club']))
random.shuffle(deck)

print("You got : ")
for i in range(5):
    print(deck[i][0], " of ", deck[i][1])
