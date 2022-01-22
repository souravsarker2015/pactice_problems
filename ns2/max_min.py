def max_min(arr):
    maxm = arr[0]
    minm = arr[0]

    for i in range(len(arr)):
        if arr[i] > maxm:
            maxm = arr[i]

        if arr[i] < minm:
            minm = arr[i]

    print(f"max: {maxm}")
    print(f"min: {minm}")


arr = [1, 2, 3, 4, 56, 7, 8, 9]
max_min(arr)
