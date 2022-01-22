list1 = [1, 2, 3, 4, 5]
# print(list1[::-1])
# arr = []
# for i in range(len(list1)-1, -1, -1):
#     arr.append(list1[i])
#
# print(arr)

start_index = 0
end_index = len(list1) - 1
# inplace operation
while end_index != start_index:
    list1[start_index], list1[end_index] = list1[end_index], list1[start_index]
    start_index += 1
    end_index -= 1

print(list1)
