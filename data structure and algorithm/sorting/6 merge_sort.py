def merge(arr):
    if len(arr) == 1:
        return

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    merge(left_half)
    merge(right_half)

    n1, n2 = len(left_half), len(right_half)

    i, j, k = 0, 0, 0

    while i < n1 and j < n2:
        if left_half[i] < right_half[j]:
            arr[k] = left_half[i]
            i += 1
            k += 1
        else:
            arr[k] = right_half[j]
            j += 1
            k += 1

    while i < n1:
        arr[k] = left_half[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = right_half[j]
        j += 1
        k += 1


if __name__ == "__main__":
    n = [1, 2, -4, -6, -1, 7, 9]
    merge(n)
    print(n)
