def fibo(n):
    if n <= 1:
        return n
    else:
        return fibo(n - 1) + fibo(n - 2)


for i in range(10):
    print(fibo(i), end=" ")

# n1 = 0
# n2 = 1
#
# for i in range(10):
#     print(n1, end=" ")
#     n3 = n1 + n2
#     n1 = n2
#     n2 = n3

# nterm = int(input("Enter how many terms ??? : "))
# n1, n2 = 0, 1
# count = 0
#
# if nterm < 0:
#     print("Enter a Positive number ")
#
# elif nterm == 1:
#     print(f"Fibonacci of {nterm} :")
#     print(n1)
#
# else:
#     print(f"Fibonacci of {nterm} terms :")
#
#     while count < nterm:
#         print(n1, end=" ")
#         nth = n1 + n2
#         n1 = n2
#         n2 = nth
#         count += 1
