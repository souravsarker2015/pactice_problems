def frequency_array(arr):
    count = {}
    for i in arr:
        if i in count:
            count[i] += 1
        else:
            count[i] = 1

    print("Frequency of elements: ")
    for key, values in count.items():
        print(f"{key} : {values}")


arr = [1, 2, 3, 45, 45, 6, 2, 3]
frequency_array(arr)
