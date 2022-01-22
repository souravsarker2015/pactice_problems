def frequency(arr):
    n = len(arr)
    count = {}
    for i in arr:
        if i in count:
            count[i] += 1
        else:
            count[i] = 1

    for key, value in count.items():
        print(f"{key} : {value}")
    print(count)


arr = [1, 1, 2, 2, 3, 3, 3, 4, 5, 5, 6, 6, 7, 8, 9]
frequency(arr)
