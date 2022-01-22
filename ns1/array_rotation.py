def array_rotate(arr, d):
    n = len(arr)
    arr2 = []
    for i in range(d, n):
        arr2.append(arr[i])

    for i in range(0, d):
        arr2.append(arr2[i])

    for i in range(n):
        print(f"{arr2[i]}", end=" ")


arr = [1, 2, 3, 4, 5, 6, 7]
d = 2  # rotate from this element
array_rotate(arr, d)
