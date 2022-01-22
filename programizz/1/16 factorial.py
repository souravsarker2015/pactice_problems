# n = int(input("Enter a Value : "))
# fact = 1
# if n < 0:
#     print("Enter a positive number : ")
#
# elif n == 0:
#     print("factorial of 0 is 1")
#
# else:
#     for i in range(1, n + 1):
#         fact = fact * i
#
# print(f"Factorial of {n} is : {fact}")
# fact = 1
# for i in range(1, 5 + 1):
#     fact = fact * i
#
# print(fact)

# n = 5
# fact = 1
# while n != 0:
#     fact = fact * n
#     n -= 1
#
# print(fact)


def rec_factorial(n):
    if n == 0:
        return 1
    else:
        return n * rec_factorial(n - 1)


if __name__ == "__main__":
    n = int(input("Enter a number :"))
    if n < 0:
        print("Enter a Positive Number")
    elif n == 0:
        print(f"Factorial of {n} :1")
    else:
        print(rec_factorial(n))
