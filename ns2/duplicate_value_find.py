def duplicate(arr):
    n = len(arr)
    temp = []
    for i in range(n):
        j = i + 1
        for k in range(j, n):
            if arr[i] == arr[k] and arr[i] not in temp:
                temp.append(arr[i])

    print(temp)


arr = [1, 2, 3, 3, 4, 4, 5, 6, 6, 7, 7, 8, 8]
duplicate(arr)
