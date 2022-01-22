def merge_array(arr1, arr2):
    n1 = len(arr1)
    n2 = len(arr2)
    arr3 = [None] * (n1 + n2)
    i, j, k = 0, 0, 0

    while i < n1 and j < n2:
        if arr1[i] < arr2[j]:
            arr3[k] = arr1[i]
            i += 1
            k += 1

        else:
            arr3[k] = arr2[j]
            j += 1
            k += 1

    while i < n1:
        arr3[k] = arr1[i]
        i += 1
        k += 1

    while j < n2:
        arr3[k] = arr3[j]
        j += 1
        k += 1

    for i in range(n1 + n2):
        print(f"{arr3[i]}", end=" ")


arr1 = [1, 2, 3, 4, 5, 6, 7]
arr2 = [2, 3, 4, 5]
merge_array(arr1, arr2)
