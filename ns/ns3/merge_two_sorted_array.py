def merge_two_sorted_array(a1, a2):
    n1, n2 = len(a1), len(a2)
    a3 = [None] * (n1 + n2)
    i, j, k = 0, 0, 0
    while (i < n1 and j < n2):
        if a1[i] <= a2[j]:
            a3[k] = a1[i]
            i += 1
            k += 1
        else:
            a3[k] = a2[j]
            j += 1
            k += 1

    while i < n1:
        a3[k] = a1[i]
        i += 1
        k += 1

    while j < n2:
        a3[k] = a2[j]
        j += 1
        k += 1

    return a3

arr1 = [1, 2, 4, 5, 6]
arr2 = [3, 7, 8, 9]
print(merge_two_sorted_array(arr1, arr2))
