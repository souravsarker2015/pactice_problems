def merge_two(list1, list2):
    n1, n2 = len(list1), len(list2)
    i, j, k = 0, 0, 0
    list3 = []
    # list1 = [1, 3, 5, 6, 9]
    # list2 = [2, 4, 5, 6, 8]
    while i < n1 and j < n2:
        if list1[i] <= list2[j]:
            list3.append(list1[i])
            i += 1
            # k += 1
        else:
            list3.append(list2[j])
            j += 1
            # k += 1
    while i < n1:
        list3.append(list1[i])
        i += 1
        # k += 1
    while j < n2:
        list3.append(list2[j])
        j += 1
        # k += 1

    return list3


list1 = [1, 3, 5, 6, 9]
list2 = [2, 4, 5, 6, 8]
print(merge_two(list1, list2))
