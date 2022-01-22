n = int(input("Enter a number : "))
total = 0

temp = n

while temp > 0:
    digit = temp % 10
    total = total + digit ** 3
    temp = temp // 10

if total == n:
    print(f"{n} is a armstrong number ")

else:
    print(f"{n} is not a armstrong number ")