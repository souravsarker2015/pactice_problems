def rec_natural(n):
    if n <= 1:
        return n

    else:
        return n + rec_natural(n - 1)


n = int(input("Enter a number : "))
if n < 0:
    print("Enter a Positive Number")
else:
    print(rec_natural(n))
