# arr = [7, 2, 3, 0, 8, 6]
# arr.sort()
#
# d = arr[0]
# temp = []
# for i in range(len(arr)):
#     while arr[i] - i != d:
#         if arr[i] - i > d:
#             temp.append(i + d)
#             d += 1
#
# print(temp)

def missing(arr):
    arr.sort()
    d = arr[0]
    temp = []

    for i in range(len(arr)):
        while arr[i] - i != d:
            if arr[i] - i > d:
                temp.append(i + d)
                d += 1
    return temp


arr = [3, 1, 15, 8]
result = missing(arr)
print(result[4])
