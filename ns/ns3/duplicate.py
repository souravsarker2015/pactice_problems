def duplicate(arr):
    n = len(arr)
    temp = []
    for i in range(n):
        j = i + 1
        for k in range(j, n):
            if arr[i] == arr[k] and arr[i] not in temp:
                temp.append(arr[i])

    return temp


arr = [1, 2, 2, 3, 5, 6, 8, 9, ]
print(duplicate(arr))
