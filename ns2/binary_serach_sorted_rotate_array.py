def rotated_array_search(arr, l, r, x):
    if r >= l:
        mid = (l + r) // 2
        if arr[mid] == x:
            return mid

        if arr[l] <= arr[mid]:
            if x >= arr[l] and x <= arr[mid]:
                return rotated_array_search(arr, l, mid - 1, x)
            else:
                return rotated_array_search(arr, mid + 1, r, x)

        else:
            if x >= arr[mid] and x <= arr[r]:
                return rotated_array_search(arr, mid + 1, r, x)
            else:
                return rotated_array_search(arr, l, mid - 1, x)
    else:
        return -1


arr = [4, 5, 6, 7, 8, 9, 1, 2, 3]
x = 3
result = rotated_array_search(arr, 0, len(arr)-1, 3)

if result != -1:
    print(f"{x} is in {result} index.")

else:
    print(f"{x} is not found.")
