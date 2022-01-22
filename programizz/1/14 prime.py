n = int(input("Enter a Number :"))
flag = True
for i in range(2, n):
    if n % i == 0:
        flag = False
        break
if flag:
    print(f"{n} is Prime")
else:
    print(f"{n} is not Prime")
