def max_min(arr):
    maxm = arr[0]
    minm = arr[0]
    for i in range(len(arr)):
        if arr[i] >= maxm:
            maxm = arr[i]

        if arr[i] < minm:
            minm = arr[i]

    print(maxm)
    print(minm)


if __name__ == "__main__":
    arr = [3, 1, 5, 9, 15, 6]
    max_min(arr)
