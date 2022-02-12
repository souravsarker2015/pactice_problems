def root_finding(x, n):
    x = float(x)
    n = int(n)

    if x >= 0 and x <= 1:
        high = 1
        low = x
    else:
        high = x
        low = 1

    epsilon = 0.00000001
    guess = (high + low) / 2
    while abs(guess ** n - x) >= epsilon:
        if guess ** n > x:
            high = guess
        else:
            low = guess
        guess = (high + low) / 2
    print(guess)


x = 5
n = 2
root_finding(x, n)
