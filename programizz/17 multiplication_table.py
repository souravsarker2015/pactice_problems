n=int(input("Enter a number :"))
k=1
print(f"multiplication table of : {k} ")
for j in range(k,11):
    for i in range(1,11):
        print(f"{j} × {i} = {i*i}")
    print(f"multiplication table of : {j+1} ")













# n = int(input("Enter a number : "))
#
# print(f"multiplication table of 1")
# for j in range(1, 11):
#     for i in range(1, 11):
#         r = j * i
#         print(f"{j} × {i} = {r}")
#
#     print()
#     print(f"multiplication table of {j+1} :")