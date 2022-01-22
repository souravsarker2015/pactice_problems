def merge_two_sorted_array(a1, a2):
    n1 = len(a1)
    n2 = len(a2)
    a3 = [None] * (n1 + n2)
    i, j, k = 0, 0, 0
    while i < n1 and j < n2:
        if a1[i] < a2[j]:
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

    for i in range(n1 + n2):
        print(f"{a3[i]}", end=" ")


arr1 = [1, 3, 5, 6, 9]
arr2 = [2, 4, 7, 8, 10]
merge_two_sorted_array(arr1, arr2)
