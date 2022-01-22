def missing_array_elements(arr):
    n = len(arr)
    d = arr[0]
    for i in range(n):
        if arr[i] - i != d:
            while d < arr[i] - i:
                print(f"{i + d}", end=" ")
                d += 1


arr = [1, 2, 8, 15, 25]
missing_array_elements(arr)
