# def missing(arr):
#     maxm = max(arr)
#     minm = min(arr)
#
#     for i in range(minm + 1, maxm):
#         if i not in arr:
#             print(i, end=" ")
#
#
def missing(arr):
    d = arr[0]
    arr1 = []
    for i in range(len(arr)):
        while arr[i] - i != d:
            if arr[i] - 1 > d:
                arr1.append(i + d)
                d += 1
    print(arr1)


if __name__ == "__main__":
    arr = [3, 4, 7, 8, 10]
    missing(arr)
