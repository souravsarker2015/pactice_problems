def duplicate(list1):
    temp = []
    for i in range(len(list1)):
        for j in range(i + 1, len(list1)):
            if list1[i] == list1[j] and list1[i] not in temp:
                temp.append(list1[i])
    return temp


list1 = [11, 11, 26, 99, 1011, 1012, 1023, 1023]
print(duplicate(list1))
