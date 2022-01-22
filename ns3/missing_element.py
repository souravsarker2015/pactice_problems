def missing_elements(arr):
    d = arr[0]  # d=1
    #
    for i in range(len(arr)):
        # i=0,1,2,3
        if arr[i] - i != d:  # 6-3 !=1
            while arr[i] - i > d:
                print(f"{i + d}", end=" ")
                d += 1  # d=2


arr = [1, 2, 3, 6, 9, 12, 15]
missing_elements(arr)
