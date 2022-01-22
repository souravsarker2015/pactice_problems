num = int(input("Enter a number : "))
flag = False
if num > 1:
    for i in range(2, num):
        if num % i == 0:
            flag = True
            break

if flag:
    print(f"{num} is not prime")

else:
    print(f"{num} is prime")

# num = 29
# flag = False
# if num > 1:
#     for i in range(2, num):
#         if num % i == 0:
#             flag = True
#             break
#
# if flag:
#     print(f"{num} is not prime")
#
# else:
#     print(f"{num} is prime")
