def binary_search_rotated(arr, l, r, x):
    if r >= l:
        mid = (l + r) // 2

        if x == arr[mid]:
            return mid

        elif (arr[l] < arr[mid]):
            if x > arr[l] and x < arr[mid]:
                return binary_search_rotated(arr, l, mid - 1, x)
            else:
                return binary_search_rotated(arr, mid + 1, r, x)

        else:
            if x > arr[mid] and x < arr[r]:
                return binary_search_rotated(arr, mid + 1, r, x)
            else:
                return binary_search_rotated(arr, l, mid - 1, x)


    else:
        return -1


arr = [4, 5, 6, 1, 2, 3]
x = 3
result = binary_search_rotated(arr, 0, len(arr) - 1, x)
if result:
    print(f"{x} is in {result} index")
else:
    print(f"{x} is not found")
