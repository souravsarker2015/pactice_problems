def sorted_rotated_array_binary_search(arr, left, right, x):
    if right >= left:
        mid = (left + right) // 2
        if x == arr[mid]:
            return mid
        else:
            if arr[left] <= arr[mid]:
                if x >= arr[left] and x <= arr[mid]:
                    return sorted_rotated_array_binary_search(arr, left, mid - 1, x)
                else:
                    return sorted_rotated_array_binary_search(arr, mid + 1, right, x)
            else:
                if x >= arr[mid] and x <= arr[right]:
                    return sorted_rotated_array_binary_search(arr, mid + 1, right, x)
                else:
                    return sorted_rotated_array_binary_search(arr, left, mid - 1, x)
    else:
        return -1


if __name__ == "__main__":
    arr = [4, 5, 1, 2, 3]
    x = 3
    result = sorted_rotated_array_binary_search(arr, 0, len(arr) - 1, x)
    if result != -1:
        print(f"{x} is in {result} index")
    else:
        print(f"{x} is not found")
