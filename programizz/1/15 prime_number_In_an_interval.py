low = 1
high = 100

for i in range(low, high + 1):
    for j in range(2, i):
        if i % j == 0:
            break
    else:
        print(i, end=" ")
