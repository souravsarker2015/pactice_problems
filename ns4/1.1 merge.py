def merge(array1, array2):
    n1, n2 = len(array1), len(array2)
    array3 = []
    i, j = 0, 0
    while i < n1 and j < n2:
        if array1[i] <= array2[j]:
            array3.append(array1[i])
            i += 1
        else:
            array3.append(array2[j])
            j += 1
    while i < n1:
        array3.append(array1[i])
        i += 1
    while j < n2:
        array3.append(array2[j])
        j += 1

    return array3


array1 = [1, 2, 3, 4, 6, 9, 15]
array2 = [10, 11, 12, 19]
print(merge(array1, array2))
