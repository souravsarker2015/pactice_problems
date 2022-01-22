# number = 12345
# count = 0
# while number != 0:
#     digit = number % 10
#     if digit:
#         count += 1
#     number = number // 10
#
# print(count)
# temp = []
# while number > 0:
#     digit = number % 10
#     temp.append(digit)
#     number = number // 10
# print(temp)
# for i in range(len(temp)):
#     print(temp[i],end="")
# print()
# print(len(temp))

number = 12345
print(len(str(number)))
count = 0

while number > 0:
    # number = number // 10
    number //=10
    count += 1
print(count)
