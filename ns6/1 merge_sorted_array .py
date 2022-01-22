def merge(a, b):
    n1, n2 = len(a), len(b)
    arr = []
    i, j = 0, 0

    while i < n1 and j < n2:
        if a[i] < b[j]:
            arr.append(a[i])
            i += 1

        else:
            arr.append(b[j])
            j += 1

    while i < n1:
        arr.append(a[i])
        i += 1

    while j < n2:
        arr.append(arr[j])
        j += 1
    return arr


if __name__ == "__main__":
    a = [1, 3, 44, 77]
    b = [2, 4, 6, 7, 8, 9, 10]
    print(merge(a, b))
