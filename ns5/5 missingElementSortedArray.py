def missingElementSortedArray(arr):
    d = arr[0]
    arr1 = []
    for i in range(len(arr)):
        while arr[i] - i != d:
            if arr[i] - i > d:
                arr1.append(i + d)
                d += 1

    return arr1


if __name__ == "__main__":
    array = [1, 6, 15, 18, 20]
    print(missingElementSortedArray(array))
