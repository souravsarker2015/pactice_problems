def root_finding(x, n):
    x, n = float(x), int(n)

    if x >= 0 and x <= 1:
        high = 1
        low = x
    else:
        high = x
        low = 1

    epsilon = 0.0000001
    guess = (high + low) / 2

    while (abs(guess ** n - x)) > epsilon:
        if guess ** n > x:
            high = guess
        else:
            low = guess

        guess = (high + low) / 2

    return guess


if __name__ == "__main__":
    x = 7
    n = 4
    print(root_finding(x, n))
