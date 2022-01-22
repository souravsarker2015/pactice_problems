def rotate_array(arr, d):
    n = len(arr)
    arr1 = []
    for i in range(d, n):
        arr1.append(arr[i])

    for j in range(0, d):
        arr1.append(arr[j])

    return arr1


arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
d = 3
print(rotate_array(arr, d))
