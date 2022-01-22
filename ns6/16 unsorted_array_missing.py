def sorted(arr):
    minm = min(arr)
    maxm = max(arr)
    arr1 = []
    for i in range(minm, maxm):
        if i not in arr:
            arr1.append(i)
    return arr1


if __name__ == "__main__":
    arr = [1, 4, 6, 9]
    result = sorted(arr)
    print(result)
    print(result[2])

# def unsorted(arr, d):
#     missing = dict()
#     for i in range(len(arr)):
#         missing[arr[i]] = 1
#
#     minm = min(arr)
#     maxm = max(arr)
#     count = 0
#     for i in range(minm + 1, maxm):
#         if i not in missing.keys():
#             count += 1
#         if count == d:
#             return i
#
#
# if __name__ == "__main__":
#     arr = [7, 6, 3, 2, 1]
#     x = 2
#     print(unsorted(arr, x))
