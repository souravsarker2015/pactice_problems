def commonElement(arr1, arr2, arr3):
    n1, n2, n3 = len(arr1), len(arr2), len(arr3)
    i, j, k = 0, 0, 0
    arr = []

    while i < n1 and j < n2 and k < n3:
        if arr1[i] == arr2[j] and arr2[j] == arr3[k]:
            arr.append(arr1[i])
            i += 1
            j += 1
            k += 1

        elif arr1[i] < arr2[j]:
            i += 1

        elif arr2[j] < arr3[k]:
            j += 1

        else:
            k += 1
    return arr


if __name__ == "__main__":
    arr1 = [1, 2, 8, 15, 19]
    arr2 = [2, 8, 16, 17]
    arr3 = [3, 8, 17]
    print(commonElement(arr1, arr2, arr3))
