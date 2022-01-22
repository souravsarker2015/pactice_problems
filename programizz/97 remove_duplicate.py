# li = [1, 2, 3, 5, 1, 1, 2, 3, 6]
#
# temp = []
# for i in range(len(li)):
#     for j in range(i + 1, len(li)):
#         if li[i] == li[j] and li[i] not in temp:
#             temp.append(li[i])
# print(temp)

# li = [1, 2, 3, 5, 1, 1, 2, 3, 6]
# print(list(set(li)))
# list_1 = [1, 2, 1, 4, 6]
# list_2 = [7, 8, 2, 1]
#
# print( (list(set(list_1)))^ (list(set(list_2))) )

list_1 = [1, 2, 1, 4, 6]
list_2 = [7, 8, 2, 1]

print(list(set(list_1) ^ set(list_2)))

#
# temp = []
# for i in range(len(li)):
#     for j in range(i + 1, len(li)-1):
#         if li[i] == li[j] :
#             li.pop(li[i])
# print(li)

