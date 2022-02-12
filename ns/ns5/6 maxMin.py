def maxMin(arr):
    maxm = arr[0]
    minm = arr[0]

    for i in range(len(arr)):
        if arr[i] >= maxm:
            maxm = arr[i]

        if arr[i] <= minm:
            minm = arr[i]

    return "Maximum: ",maxm ,'Minimum :', minm


if __name__ == "__main__":
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    print(maxMin(arr))