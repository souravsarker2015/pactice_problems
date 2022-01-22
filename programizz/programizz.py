# 13 largest number among three numbers
n1 = int(input("Enter the number 1 :"))
n2 = int(input("Enter the number 2 :"))
n3 = int(input("Enter the number 3 :"))

if n1 >= n2 and n1 >= n3:
    print(f"largest number is {n1}")
elif n2 >= n1 and n2 >= n3:
    print(f"largest number is {n2}")
else:
    print(f"largest number is {n3}")

# 12 leap year
# year = int(input("Enter the Year : "))
#
# if year % 4 == 0:
#     if year % 100 == 0:
#         if year % 400 == 0:
#             print(f"{year} is Leap Year.")
#         else:
#             print(f"{year} is not Leap Year.")
#     else:
#         print(f"{year} is Leap Year.")
#
# else:
#     print(f"{year} is not Leap Year.")

# 11 odd even
# number = int(input("enter the number: "))
# if number % 2 == 0:
#     print(f"{number} is even")
# # elif number % 2 != 0:
# #     print(f"{number} is odd")
# else:
#     print(f"{number} is odd")

# 10 number positive negative or zero
# number = int(input("Enter the test number: "))
# if number < 0:
#     print(f"{number}  is negative")
# elif number > 0:
#     print(f"{number} is positive")
# else:
#     print(f"{number} is zero")

# 9 celcious to firenhight
# c = float(input("Enter the temperature in celcius :"))
# f = ((9 / 5) * c) + 32
# print(f"{c} degree celcius = {f} degree firenhight ")
# print(f"%0.2f degree celcius = %.2f degree firenhight " % (c, f))

# 8 kilometer to miles
# kilo = float(input("enter the value in kilometer: "))
# miles = kilo * 0.62
# print(f"result in miles: ", miles)
# print(f"%0.2f kilometers = %0.2f miles " % (kilo, miles))

# 7 random number
# import random
#
# for i in range(5):
#     number = random.randint(50, 55)
#     print(number)

# 6 swap

# a = 60
# b = 85
# print(f"before:  a={a} and b={b}")
# temp = a
# a = b
# b = temp
# print(f"after:  a={a} and b={b}")

# 5

# import cmath
# # ax**2 +bx +c
# a = 1
# b = 5
# c = 6
# d = (b ** 2) - (4 * a * c)
# s1 = (-b + cmath.sqrt(d)) / 2 * a
# s2 = (-b - cmath.sqrt(d)) / 2 * a

# print(f"solutions are {s1} and {s2}")
# print("solutions are {0} and {1}".format(s1, s2))
# 4.1

# import math

# a = int(input("enter the value of side 1 :"))
# b = int(input("enter the value of side 1 :"))
# c = int(input("enter the value of side 1 :"))
# s = (a + b + c) / 2
# # area = math.sqrt(s * (s - a) * (s - b) * (s - c))
# area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
# print("area: ", area)

# 4
# height = int(input("Enter the height of the triangle: "))
# base = int(input("Enter the base of the triangle: "))
# area = .5 * height * base
# print(f"Area: ", area)

# 3
# import math
# n1 = int(input("Enter the number :"))
# ans = math.sqrt(n1)
# print(f"square root of {n1} : ", ans)

# 2
# n1 = int(input("Enter a Number: "))
# n2 = int(input("Enter a another: "))
# addition = n1 + n2
# print(addition)

# 1
# print("Hello world")
