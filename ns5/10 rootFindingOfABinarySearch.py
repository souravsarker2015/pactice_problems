def root_finding(x, n):
    x, n = float(x), int(n)
    if x >= 0 and x <= 1:
        high = 1
        low = x
    else:
        high = x
        low = 1

    guess = (high + low) / 2
    epsilon = 0.00000001

    while (abs(guess ** n - x)) > epsilon:
        if guess ** n > x:
            high = guess
        else:
            low = guess
        guess = (high + low) / 2

    return guess


if __name__ == "__main__":
    x = 5
    n = 2
    print(root_finding(x, n))
