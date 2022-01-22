def insert(arr, x):
    i = 0
    for i in range(len(arr)):
        if x < arr[i]:
            break
    arr = arr[:i] + [x] + arr[i:]
    print(arr)


if __name__ == "__main__":
    arr = [1, 3, 4, 6, 8, 10]
    x = 7
    insert(arr, x)
