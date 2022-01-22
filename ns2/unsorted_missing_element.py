def unsorted_array_missing_element(a, k):
    n = len(a)
    missing = dict()
    for i in range(n):
        missing[a[i]] = 1

    count = 0
    maxm = max(a)
    minm = min(a)
    for i in range(minm + 1, maxm):
        if i not in missing.keys():
            count += 1
        if count == k:
            return i

    return -1


arr = [1, 3, 2, 8, 6]
k = 2
r = unsorted_array_missing_element(arr, k)
print(r)
