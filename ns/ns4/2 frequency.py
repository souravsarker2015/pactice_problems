def frequency(arr):
    count = {}

    for i in arr:
        if i in count:
            count[i] += 1
        else:
            count[i] = 1

    return count


array = [11, 11, 22, 22, 33, 66, 99, 99]
print(frequency(arr=array))
