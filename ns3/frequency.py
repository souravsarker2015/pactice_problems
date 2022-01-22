def ferquency_of_arary(arr):
    count = {}
    for i in arr:
        if i in count:
            count[i] += 1
        else:
            count[i] = 1

    for key, value in count.items():
        print(f"{key} : {value}")


arr = [1, 1, 1, 1, 1, 2, 5, 3, 6, 4, 2]
ferquency_of_arary(arr)
