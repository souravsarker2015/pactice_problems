n = int(input("Enter a Number :"))
n1 = int(input("Enter the Power :"))

result = pow(n, n1)
print(f"The of {n}^{n1} : {result} ")
# res = 1
# while n1 != 0:
#     res = res * n
#     n1 = n1 - 1
# print(res)
res = 1
for i in range(n1, 0, -1):
    res = res * n
    n1 -= 1
print(res)
