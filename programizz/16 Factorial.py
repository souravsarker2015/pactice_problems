n = int(input("Enter a number :"))
res=1
for i in range(1,n+1):
    res = res * i
print(res)







# def fac(num):
#     if num == 1:
#         return 1
#     else:
#         res = num * fac(num - 1)
#         return res
#
# print(fac(5))

# n = int(input("Enter a number : "))
# factorial = 1
# if n < 0:
#     print(f"factorial is not number less than zero")
#
# elif n == 0:
#     print(f"factorial of {n} = 1")
#
# else:
#     for i in range(1, n + 1):
#         factorial = factorial * i
#     print(f"factorial of {n} = {factorial}")
