def frequency_array_element(arr):
    count = {}

    for i in arr:
        if i in count:
            count[i] += 1
        else:
            count[i] = 1

    # for key, value in count.items():
    #     print(f"{key} : {value}")

    print(count)


arr = [1, 1, 2, 3, 2, 5, 4, 5, 2]
frequency_array_element(arr)
