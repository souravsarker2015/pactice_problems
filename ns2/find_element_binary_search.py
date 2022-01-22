def binary_search(arr, l, r, x):
    if r >= l:
        mid = (l + r) // 2
        if arr[mid] == x:
            return mid
        if x < arr[mid]:
            return binary_search(arr, l, mid - 1, x)
        else:
            return binary_search(arr, mid + 1, r, x)

    else:
        return -1
arr = [1, 2, 34, 45, 65, 75]
x = 75
result = binary_search(arr, 0, len(arr) - 1, x)

if result != -1:
    print(f"{x} is the :{result} index")

else:
    print(f"{x} is not found in the array")
