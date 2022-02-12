def common(a1, a2, a3):
    n1, n2, n3 = len(a1), len(a2), len(a3)
    i, j, k = 0, 0, 0
    while i < n1 and j < n2 and k < n3:
        if a1[i] == a2[j] and a2[j] == a3[k]:
            print(a1[i], end=" ")
            i += 1
            j += 1
            k += 1

        elif a1[i] < a2[j]:
            i += 1

        elif a2[j] < a3[k]:
            j += 1
        else:
            k += 1


a1 = [1, 2, 3, 4, 5, 56, 66]
a2 = [1, 2, 3, 4, 5, 56, 66]
a3 = [1, 2, 3, 4, 5, 56, 66]
common(a1, a2, a3)
