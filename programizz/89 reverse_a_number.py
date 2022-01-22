n = 689
temp = []
while n >= 1:
    digit = n % 10
    temp.append(digit)
    n = n // 10

for i in temp:
    print(i, end="")

n1 = 689
rev = 0
while n1 >= 1:
    digit = n1 % 10
    rev = rev * 10 + digit
    n1 = n1 // 10

print(rev)
