def binary_search_rotated_array(arr, l, r, x):
    if r >= l:
        mid = (l + r) // 2
        if x == arr[mid]:
            return mid

        if arr[l] < arr[mid]:
            if x > arr[l] and x < arr[mid]:
                return binary_search_rotated_array(arr, l, mid - 1, x)
            else:
                return binary_search_rotated_array(arr, mid + 1, r, x)

        else:
            if x > arr[mid] and x < arr[r]:
                return binary_search_rotated_array(arr, mid + 1, r, x)
            else:
                return binary_search_rotated_array(arr, l, mid - 1, x)
    else:
        return -1


arr = [3, 4, 5, 6, 1, 2]
x = 1
res = binary_search_rotated_array(arr, 0, len(arr)-1, x)

if res != -1:
    print(f"{x} is in {res} index")

else:
    print(f"{x} is not found")
