def missing(arr):
    d = arr[0]
    temp = []
    for i in range(len(arr)):
        while arr[i] - i != d:
            if arr[i] - i > d:
                r = i + d
                temp.append(r)
                d += 1
    return temp


arr = [1, 2, 3, 6, 9, 15]
result = missing(arr)
print(result)


# list1 = [1, 2, 4, 5]
#
# mid = len(list1) // 2
# print(list1[mid])
