def max_min(arr):
    min = arr[0]
    max = arr[0]

    for i in range(len(arr)):
        if arr[i] > max:
            max = arr[i]
        if arr[i] < min:
            min = arr[i]

    print(f"maximum= {max}")
    print(f"minimum= {min}")


arr = [1, 2, 3, 4, 5, 6, 78, 5, 6, 9, 2, 5, 6, 88]
max_min(arr)
