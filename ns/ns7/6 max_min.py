def max_min(arr):
    minm = arr[0]
    maxm = arr[0]
    for i in arr:
        if i < minm:
            minm = i

        if i > maxm:
            maxm = i

    print(minm)
    print(maxm)


if __name__ == "__main__":
    arr = [1, 5, 6, 9]
    max_min(arr)
