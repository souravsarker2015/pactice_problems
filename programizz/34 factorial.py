def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n - 1)


n = int(input("Enter a Number :"))
if n < 0:
    print("Enter a Positive Number")
elif n == 0:
    print(1)
else:
    print(factorial(n))
