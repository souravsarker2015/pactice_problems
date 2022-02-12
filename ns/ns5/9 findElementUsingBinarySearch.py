def findElementUsingBinarySearch(arr, l, r, x):
    if r >= l:
        mid = (l + r) // 2

        if x == arr[mid]:
            return mid

        else:
            if x < arr[mid]:
                findElementUsingBinarySearch(arr, l, mid - 1, x)
            else:
                findElementUsingBinarySearch(arr, mid + 1, r, x)

    else:
        return -1


if __name__ == "__main__":
    arr = [1, 2, 3, 4, 5, 6]
    x = 5
    result = findElementUsingBinarySearch(arr, 0, len(arr) - 1, x)

    if result != -1:
        print(f"{x} is in {result} index ")

    else:
        print(f"{x} not found")

#
# def binarySearch(arr, l, r, x):
#     # Check base case
#     if r >= l:
#
#         mid = l + (r - l) // 2
#
#         # If element is present at the middle itself
#         if arr[mid] == x:
#             return mid
#
#         # If element is smaller than mid, then it
#         # can only be present in left subarray
#         elif arr[mid] > x:
#             return binarySearch(arr, l, mid - 1, x)
#
#         # Else the element can only be present
#         # in right subarray
#         else:
#             return binarySearch(arr, mid + 1, r, x)
#
#     else:
#         # Element is not present in the array
#         return -1
#
#
# # Driver Code
# arr = [2, 3, 4, 10, 40]
# x = 40
#
# # Function call
# result = binarySearch(arr, 0, len(arr) - 1, x)
#
# if result != -1:
#     print("Element is present at index % d" % result)
# else:
#     print("Element is not present in array")
