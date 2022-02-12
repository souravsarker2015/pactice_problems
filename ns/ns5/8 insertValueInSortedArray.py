def insert(arr, x):
    i = 0
    for i in range(len(arr)):
        if arr[i] >= x:
            break
    return arr[:i] + [x] + arr[i:]


if __name__ == "__main__":
    array = [2, 3, 56, 77, 88]
    d = 4
    print(insert(array, d))
