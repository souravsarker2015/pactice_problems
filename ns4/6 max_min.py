list1 = [1, 2, 3, 4, 5, 6, 55, 99, 55, 1, 6]
max = list1[0]
min = list1[0]

for i in range(len(list1)):
    if list1[i] >= max:
        max = list1[i]

    if list1[i] <= min:
        min = list1[i]

print(f"max : {max} , min : {min}")
