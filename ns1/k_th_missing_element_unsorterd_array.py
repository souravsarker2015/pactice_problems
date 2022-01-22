def missing_element(arr, k):
    n = len(arr)
    missing = dict()
    count = 0

    for i in range(n):
        missing[arr[i]] = 1

    maxm = max(arr)
    minm = min(arr)

    for i in range(minm + 1, maxm):
        if i not in missing.keys():
            count += 1
        if count == k:
            return i
    return -1


arr = [2, 10, 9, 4]
k = 5
print(missing_element(arr, k))
