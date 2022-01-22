n1 = 60
n2 = 24
gcd = 0
if n1 > n2:
    small = n2

else:
    small = n1

for i in range(1, small + 1):
    if (n1 % i == 0) and (n2 % i == 0):
        gcd = i
print(gcd)
print((n1*n2)//gcd)

# n3 = 60
# n4 = 30
#
# while (n4 != 0):
#     rem = (n3 % n4)
#     n3 = n4
#     n4 = rem
# print(n3)
