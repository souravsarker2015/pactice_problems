def rotate(list1, d):
    list2 = []

    for i in range(d, len(list1)):
        list2.append(list1[i])

    for j in range(0, d):
        list2.append(list1[j])

    return list2


list1 = [1, 2, 3, 4, 5, 6]
d = 2
print(rotate(list1, d))
