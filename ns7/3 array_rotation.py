def rotation(arr, x):
    arr1 = []
    for i in range(x, len(arr)):
        arr1.append(arr[i])
    i = 0
    for i in range(0, x):
        arr1.append(arr[i])

    return arr1


if __name__ == "__main__":
    arr = [1, 2, 3, 4, 5, 6]
    x = 3
    print(rotation(arr, x))
