
for num in range(100, 501):
    temp = num
    sum = 0
    order=len(str(num))
    while temp > 0:
        digit = temp % 10
        sum = sum + digit ** 3
        temp=temp//10

    if num==sum:
        print(num,end=" ")



# # Program to check Armstrong numbers in a certain interval
#
# lower = 100
# upper = 2000
#
# for num in range(lower, upper + 1):
#
#     # order of number
#     order = len(str(num))
#     # print(order)
#
#     # initialize sum
#     sum = 0
#
#     temp = num
#     while temp > 0:
#         digit = temp % 10
#         sum += digit ** order
#         temp //= 10
#
#     if num == sum:
#         print(num)


# low = 200
# high = 300
# total = 0
# for i in range(1,10):
#     temp = i
#     order=len(str(i))
#     # print(order)
#     while temp > 0:
#         # print(temp)
#         digit = temp % 10
#         total = total + pow(digit,3)
#
#         temp = temp // 10
#
#     # if i == total:
#     #     print(i, end=" ")
#
# # num = int(input("Enter a Number : "))
# # total = 0
# # temp = num
# # while temp > 0:
# #     print(temp)
# #     digit = temp % 10
# #     total = total + (digit ** 3)
# #     print(total)
# #     temp = temp // 10
# #
# # if total == num:
# #     print("Armstrong")
# #
# # else:
# #     print("Not Armstrong")
