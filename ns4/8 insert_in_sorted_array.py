def insert(arr, x):
    i = 0
    for i in range(len(arr)):
        if arr[i] >= x:
            break
    arr = arr[:i] + [x] + arr[i:]
    print(arr)


arr = [1, 2, 3, 6, 8]
x = 4
insert(arr, x)
