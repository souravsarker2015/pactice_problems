def binary_search(arr, l, r, x):
    if r >= l:
        mid = (l + r) // 2
        if x == arr[mid]:
            return mid

        if x < arr[mid]:
            return binary_search(arr, l, mid - 1, x)
        else:
            return binary_search(arr, mid + 1, r, x)
    else:
        return -1


if __name__ == "__main__":
    arr = [1, 2, 3, 6, 7, 9, 15]
    x = 15
    result = binary_search(arr, 0, len(arr)-1, x)

    if result != -1:
        print(f"{x} is in {result} index")
    else:
        print(f"{x} is not found")
