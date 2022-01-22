def array_rotation(arr, d):
    n = len(arr)
    temp = []
    for i in range(d, n):
        temp.append(arr[i])
    i = 0
    for i in range(0, d):
        temp.append(arr[i])

    for i in range(n):
        print(f"{temp[i]}", end=" ")


arr = [1, 2, 3, 4, 5, 6, 7]
array_rotation(arr, 3)
