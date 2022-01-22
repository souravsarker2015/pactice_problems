my_list = [1, 2, 4, 6, 8, 9, 7, 25, 6, 5, 65, 1, 2]

result = list(filter(lambda x: (x % 2 == 0), my_list))
print(result)

temp = []
for i in range(len(my_list)):
    if my_list[i] % 2 == 0:
        temp.append(my_list[i])

print(temp)

print(list(filter(lambda x: x % 2 == 0, my_list)))
