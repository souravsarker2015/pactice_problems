n = int(input("Enter a multiplication table number :"))
print(f"Multiplication table of {n} :")
for i in range(1, 11):
    result = n * i
    print(f"{n} × {i} : {result}")
