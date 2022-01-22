def array_rotation(arr, d):
    arr1 = []
    for i in range(d, len(arr)):
        arr1.append(arr[i])

    for j in range(0, d):
        arr1.append(arr[j])

    return arr1


if __name__ == "__main__":
    arr = [1, 2, 3, 4, 5, 6, 7]
    print(array_rotation(arr, 4))
