def missing(arr):
    minm = arr[0]
    maxm = arr[0]

    for i in range(len(arr)):
        if arr[i] < minm:
            minm = arr[i]

        if arr[i] > maxm:
            maxm = arr[i]

    for i in range(minm, maxm):
        if i not in arr:
            print(i, end=" ")


if __name__ == "__main__":
    arr = [1, 4, 7, 9]
    missing(arr)
