total = 0

for i in range(11):
    total = total + i

print(total)

# using recursion:

# def sum_natural(n):
#     sum = 0
#     if n < 1:
#         return n
#     else:
#         sum = n + sum_natural(n - 1)
#         return sum
#
#
# print(sum_natural(10))
