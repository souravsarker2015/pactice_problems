def array_rotation(arr, d):
    n = len(arr)
    temp = []
    for i in range(d, n):
        temp.append(arr[i])

    for j in range(0, d):
        temp.append(arr[j])

    for k in range(n):
        print(f"{temp[k]}", end=" ")


arr = [1, 2, 3, 4, 5, 6, 7]
d = 4
array_rotation(arr, d)
