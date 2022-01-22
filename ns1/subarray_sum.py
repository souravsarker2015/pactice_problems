def sub_array_sum(arr):
    max_sum = 0
    current_sum = 0

    current_start = 0
    current_end = 0

    max_start = 0
    max_end = 0

    for i in range(len(arr)):
        current_sum = current_sum + arr[i]
        current_end = i
        if current_sum < 0:
            current_sum = 0
            current_start = current_end + 1

        if max_sum < current_sum:
            max_sum = current_sum
            max_start = current_start
            max_end = current_end

    print(f"Max subarray start index : {max_start} ")
    print(f"Max subarray end index : {max_end} ")
    print(f"Max subarray sum : {max_sum} ")


arr = [-1, 2, 3, 64, 5, -8, 8]
sub_array_sum(arr)
