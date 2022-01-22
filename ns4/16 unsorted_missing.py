def missing_elements(arr, n):
    missing = dict()
    for i in range(len(arr)):
        missing[arr[i]] = 1

    minm = min(arr)
    maxm = max(arr)
    count = 0

    for i in range(minm +1, maxm):
        if i not in missing:
            count += 1
        if count==n:
            return i



arr = [6, 8, 4, 2, 1, 9, 7, 15]
d = 3
print(missing_elements(arr, d))
