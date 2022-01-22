def duplicate_value(arr):
    n = len(arr)
    arr1 = []
    for i in range(n):
        k = i + 1
        for j in range(k, n):
            if arr[i] == arr[j] and arr[i] not in arr1:
                arr1.append(arr[i])
    for i in range(len(arr1)):
        print(f"{arr1[i]}", end=" ")


arr = [1, 1, 2, 3, 5, 4, 5, 6, 7, 7]
duplicate_value(arr)
