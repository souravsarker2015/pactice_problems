n1 = 60
n2 = 30

if n1 > n2:
    big = n1
else:
    big = n2

while (True):
    if (big % n1) == 0 and big % n2 == 0:
        lcm = big
        break
    big = big + 1

print(lcm)
