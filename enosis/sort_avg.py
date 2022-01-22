def print_avg(arr):
    arr2 = []
    arr.sort()
    for i in range(1, len(arr) - 1):
        arr2.append(arr[i])

    return (arr2[0] + arr2[1]) / 2


num = [8, 7, 1, 9]
print(print_avg(num))
