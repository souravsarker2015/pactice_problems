def common_elements_find(a, b, c):
    n1, n2, n3 = len(a), len(b), len(c)
    i, j, k = 0, 0, 0
    arr = []
    while i < n1 and j < n2 and k < n3:
        if a[i] == b[j] and b[j] == c[k]:
            arr.append(a[i])
            i += 1
            j += 1
            k += 1

        elif a[i] < b[j]:
            i += 1
        elif b[j] < c[k]:
            j += 1
        else:
            k += 1
    return arr


arr1 = [1, 2, 3, 4, 5, 6, 7, 8]
arr2 = [2, 3, 4, 7, 8, 990]
arr3 = [4, 5, 6, 7, 8, 9, 00, 0, 88, ]

print(common_elements_find(arr1,arr2,arr3))