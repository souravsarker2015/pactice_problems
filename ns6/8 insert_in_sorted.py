def insert(arr, x):
    i = 0
    for i in range(len(arr)):
        if arr[i] > x:
            break
    arr1 = arr[:i] + [x] + arr[i:]
    print(arr1)


if __name__ == "__main__":
    array = [5, 6, 9]
    insert(array, 1)
