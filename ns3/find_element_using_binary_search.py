def binary_search(arr, l, r, x):
    if r >= l:
        mid = (l + r) // 2
        if x == arr[mid]:
            return mid

        elif (x < arr[mid]):
            return binary_search(arr, l, mid - 1, x)

        else:
            return binary_search(arr, mid + 1, r, x)

    else:
        return -1


arr = [1, 2, 3, 5, 6, 9]
x = 6
res = binary_search(arr, 0, len(arr) - 1, x)

if res != -1:
    print(f"{x} is in {res} index")

else:
    print(f"{x} is not found")
