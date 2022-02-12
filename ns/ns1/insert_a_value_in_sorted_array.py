def insert_a_value_in_sorted_array(arr, d):
    for i in range(len(arr)):
        if arr[i] > d:
            break
    arr = arr[:i] + [d] + arr[i:]
    print(arr)


arr = [1, 3, 7, 9, 15]
d = 12
insert_a_value_in_sorted_array(arr, d)
