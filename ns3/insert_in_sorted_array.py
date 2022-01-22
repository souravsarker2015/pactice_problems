def insert_value(arr, x):
    i = 0
    for i in range(len(arr)):
        if arr[i] >= x:
            break
    arr = arr[:i] + [x] + arr[i:]
    return arr


arr = [1, 3, 6, 7, 9]
x = 8
print(insert_value(arr, x))
