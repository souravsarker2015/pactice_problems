def merge(array1, array2):
    n1, n2 = len(array1), len(array2)
    i, j, k = 0, 0, 0
    array3 = []

    while i < n1 and j < n2:
        if array1[i] < array2[j]:
            array3.append(array1[i])
            i += 1
            # j += 1

        else:
            array3.append(array2[j])
            j += 1
            # j += 1

    while i < n1:
        array3.append(array1[i])
        i += 1

    while j < n2:
        array3.append(array2[j])
        j += 1

    return array3


if __name__ == "__main__":
    array1 = [1, 2, 3, 7, 8, 9]
    array2 = [4, 5, 6, 10]
    result = merge(array1, array2)
    print(result)
