def missing_elements_sorted_array(arr):
    n = len(arr)
    d = arr[0]
    for i in range(n):
        if arr[i] - i != d:
            while d < arr[i] - i:
                print(f"{d + i}", end=" ")
                d += 1


arr = [1, 2, 3, 4, 6, 7, 9, 15]
missing_elements_sorted_array(arr)
