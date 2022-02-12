def mergeTwoSortedArray(arr1, arr2):
    n1, n2 = len(arr1), len(arr2)
    i, j = 0, 0
    arr3 = []

    while i < n1 and j < n2:
        if arr1[i] <= arr2[j]:
            arr3.append(arr1[i])
            i += 1

        else:
            arr3.append(arr2[j])
            j += 1

    while i < n1:
        arr3.append(arr1[i])
        i += 1

    while j < n2:
        arr3.append(arr2[j])
        j += 1

    return arr3


if __name__ == '__main__':
    arr1 = [1, 2, 4, 56, 88,99]
    arr2 = [3, 222, 444, 566, 888]
    print(mergeTwoSortedArray(arr1, arr2))
