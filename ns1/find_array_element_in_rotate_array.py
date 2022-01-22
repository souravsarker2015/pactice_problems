def find_array_element_in_rotate_array(arr, l, r, x):
    if r >= l:
        mid = (l + r) // 2
        if arr[mid] == x:
            return mid

        if arr[l] <= arr[mid]:
            if x >= arr[l] and x <= arr[mid]:
                return find_array_element_in_rotate_array(arr, l, mid - 1, x)
            return find_array_element_in_rotate_array(arr, mid + 1, r - 1, x)

        else:
            if x >= arr[mid] and x <= arr[r]:
                return find_array_element_in_rotate_array(arr, mid + 1, r, x)
            return find_array_element_in_rotate_array(arr, l, mid - 1, x)

    else:
        return -1


arr = [4, 5, 6, 7, 8, 9, 1, 2, 3]
x = 2
result = find_array_element_in_rotate_array(arr, 0, len(arr) - 1, x)

if result != -1:
    print(f"Element is in  index", result)
else:
    print("Element is not found")
