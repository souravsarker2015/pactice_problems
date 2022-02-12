def unsorted_aray_missing_element(arr, k):
    missing = dict()
    for i in range(len(arr)):
        missing[arr[i]] = 1

    count = 0
    maxm = max(arr)
    minm = min(arr)
    for i in range(minm + 1, maxm):
        if i not in missing.keys():
            count += 1
        if count == k:
            return i

    return -1


arr = [1, 4, 56, 7, 42, 7, 88, 9]
k = 5
r = unsorted_aray_missing_element(arr, k)
print(r)
