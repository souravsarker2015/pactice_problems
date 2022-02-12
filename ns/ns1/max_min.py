def max_min_array(arr):
    max = arr[0]
    min = arr[0]

    for i in range(len(arr)):
        if arr[i] >= max:
            max = arr[i]
    print(f"Maximum element of array is {max} ")

    for i in range(len(arr)):
        if arr[i] <= min:
            min = arr[i]
    print(f"Minimum element of the array is {min}")


arr = [1, 23, 5, 56, 4, 8, 2, 5, 6]
max_min_array(arr)
