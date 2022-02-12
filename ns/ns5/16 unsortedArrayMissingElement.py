def unsortedArrayMissingElement(arr, d):
    missing = dict()

    for i in range(len(arr)):
        missing[arr[i]] = 1

    maxm = max(arr)
    minm = min(arr)
    count = 0
    for i in range(minm + 1, maxm):
        if i not in missing.keys():
            count += 1
        if count == d:
            return i


if __name__ == "__main__":
    array = [7, 6, 3, 2, 1]
    print(unsortedArrayMissingElement(array, 2))

# def missing(arr):
#     temp = []
#     d = arr[0]
#
#     for i in range(len(arr)):
#         while arr[i] - i != d:
#             if arr[i] - i > d:
#                 temp.append(i + d)
#                 d += 1
#     return temp
#
#
# arr = [3, 1, 15, 8]
# arr.sort()
#
# print(missing(arr))
