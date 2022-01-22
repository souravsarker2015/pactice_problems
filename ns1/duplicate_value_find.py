def duplicate_value_find(arr):
    n = len(arr)
    arr1=[]
    for i in range(n):
        j = i + 1
        for k in range(j,n):
            if arr[i] == arr[k] and arr[i] not in arr1:
                arr1.append(arr[i])

    print(arr1)


arr = [1, 2, 2, 3, 3, 4, 5, 6, 5]
duplicate_value_find(arr)
