def common_element(a1, a2, a3):
    n1 = len(a1)
    n2 = len(a2)
    n3 = len(a3)
    i, j, k = 0, 0, 0

    while i < n1 and j < n2 and k < n3:
        if a1[i] == a2[j] and a2[j] == a3[k]:
            print(a1[i])
            i += 1
            j += 1
            k += 1

        elif a1[i] < a2[j]:
            i += 1

        elif a2[j] < a3[k]:
            j += 1

        else:
            k += 1


# arr1 = [1, 2, 3, 6]
# arr2 = [2, 3, 4, 6]
# arr3 = [1, 1, 2, 6]
arr1 = [1, 2, 3, 5, 6, 8, 9, 9, 45]
arr2 = [1, 2, 3, 5, 6, 45, 65, 99]
arr3 = [1, 5, 6, 6, 45, 65, 99, 101]
common_element(arr1, arr2, arr3)
