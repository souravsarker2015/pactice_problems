def missing(arr):
    d = arr[0]
    for i in range(len(arr)):
        while arr[i] - i != d:
            if arr[i] - i > d:
                print(i + d,end=" ")
                d += 1


if __name__ == "__main__":
    arr = [1, 5, 8, 13]
    missing(arr)
