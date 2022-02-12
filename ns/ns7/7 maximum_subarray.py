def maximum_subarray(arr):
    current_sum = 0
    maximum_sum = 0

    current_start = 0
    current_end = 0

    maximum_start = 0
    maximum_end = 0

    for i in range(len(arr)):
        current_sum = current_sum + arr[i]
        current_end = i
        if current_sum < 0:
            current_sum = 0
            current_start = current_end + 1

        if maximum_sum<current_sum:
            maximum_sum = current_sum
            maximum_start = current_start
            maximum_end = current_end

    print(maximum_start)
    print(maximum_end)
    print(maximum_sum)



arr = [1, 5, 6, 7, 9]
maximum_subarray(arr)
