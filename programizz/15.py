for i in range(1, 200):
    if i > 1:
        for j in range(2, i):
            if i % j == 0:
                break
        else:
            print(i, end=" ")













# lowest = 900
# highest = 1000
#
# for num in range(lowest, highest+1):
#     if num > 1:
#         for i in range(2, num):
#             if num % i == 0:
#                 break
#         else:
#             print(num)
