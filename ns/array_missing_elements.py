# find missing elements in a sorted array.
def array_missing_element(arr):
    n = len(arr)
    d = arr[0]
    for i in range(n):
        if arr[i] - i != d:
            while d < arr[i] - i:
                print(f"{i + d}", end=" ")
                d += 1


arr = [1, 2, 5, 6, 9]
array_missing_element(arr)
