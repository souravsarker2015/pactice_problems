def sub_array(arr):
    current_sum = 0
    max_sum = 0
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

        elif current_sum > max_sum:
            max_sum = current_sum
            max_start = current_start
            max_end = current_end
    print(f"maximum subarray sum : {max_sum}")
    print(f"maximum subarray sum start : {max_start}")
    print(f"maximum subarray sum end : {max_end}")


arr = [1, 2, 3, 6, 5, 8, 9, 5, 64]
sub_array(arr)
