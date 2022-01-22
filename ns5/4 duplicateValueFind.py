def duplicateValueFind(arr):
    arr1 = []

    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j] and arr[i] not in arr1:
                arr1.append(arr[i])

    return arr1


if __name__ == "__main__":
    arr = [1, 2, 3, 4, 5, 5, 6, 6, 6, 6]
    print(duplicateValueFind(arr))
