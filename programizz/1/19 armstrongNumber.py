# n = int(input("Enter a Number :"))
# res = 0
# temp = n
# while temp > 0:
#     digit = temp % 10
#     res = res + digit ** 3
#     temp = temp // 10
#
# if temp == res:
#     print(f"{n} is a armstrong number")
#
# else:
#     print(f"{n} is not a armstrong number")

for i in range(100, 500):
    temp = i
    res = 0
    while temp > 0:
        digit = temp % 10
        res = res + digit ** 3
        temp = temp // 10
    if i == res:
        print(i, end=" ")
    else:
        continue
