def common(a, b, c):
    n1, n2, n3 = len(a), len(b), len(c)
    # a = [2, 5, 8, 9]
    # b = [1, 2, 3, 4, 5, 6, 7]
    # c = [2, 3, 45, 56]
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


if __name__ == "__main__":
    a = [2, 5, 8, 9]
    b = [1, 2, 3, 4, 5, 6, 7]
    c = [2, 3, 45, 56]
    print(common(a, b, c))
