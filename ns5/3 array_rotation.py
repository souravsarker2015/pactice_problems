def array_rotation(arr, d):
    n = len(arr)
    arr1 = []
    for i in range(d, n):
        arr1.append(arr[i])

    for j in range(0, d):
        arr1.append(arr[j])

    return arr1


if __name__ == "__main__":
    arr = [1, 2, 3, 4, 6, 8, 9, 0]
    print(array_rotation(arr, 4))

