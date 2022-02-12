def insert_value_in_sorted_array(arr, d):
    for i in range(len(arr)):
        if arr[i] > d:
            break
    arr = arr[:i] + [d] + arr[i:]
    print(arr)

arr = [1, 2, 3, 5, 7, 8, 9]
d = 8
insert_value_in_sorted_array(arr, d)
