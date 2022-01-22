def shift_zero(arr):
    arr1 = []
    arr2 = []
    for i in arr:
        if i == 0:
            arr2.append(i)
        else:
            arr1.append(i)
    arr = arr1 + arr2
    print(arr)


if __name__ == "__main__":
    arr = [1, 2, 3, 0, 0, 5, 6, 8]
    shift_zero(arr)
