# def power_two(n):
#     if n == 0:
#         return False
#
#     else:
#         while n != 1:
#             if n % 2 != 0:
#                 return False
#             n = n // 2
#         return True
#
#
# n = 32
# result = power_two(n)
# if result:
#     print(f"{n} is power of two")
#
# else:
#     print(f"{n} is not power of two")


# def power(n):
#     if n == 0:
#         return False
#     else:
#         while n != 1:
#             if n % 2 != 0:
#                 return False
#             n = n // 2
#         return True
#
#
# n = 32
# res = power(n)
# if res:
#     print(f"{n} is power of two")
# else:
#     print(f"{n} is not power of two")

#
# def root(x, n):
#     x = float(x)
#     n = int(n)
#     if x >= 0 and x <= 1:
#         high = 1
#         low = x
#     else:
#         high = x
#         low = 1
#
#     guess = (high + low) / 2
#     epsilon = 0.0000001
#
#     while abs(guess ** n - x) > epsilon:
#         if guess ** n > x:
#             high = guess
#         else:
#             low = guess
#         guess = (high + low) / 2
#     return guess
#
#
# x = 5
# n = 3
# print(f"{root(x, n)}")

def power(n):
    if n == 0:
        return False
    else:
        while n != 1:
            if n % 2 != 0:
                return False
            n = n // 2
        return True


if __name__ == '__main__':
    n = 32
    res = power(n)
    if res:
        print(f"{n} is power of two")
    else:
        print(f"{n} is not power of two")
