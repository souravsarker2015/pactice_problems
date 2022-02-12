def subarray_sum(arr):
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
        else:
            max_sum = current_sum
            max_start = current_start
            max_end = current_end
    print(max_sum)
    print(max_start)
    print(max_end)


arr = [1, 2, 3, 6, 7, - 45, -12]
subarray_sum(arr)


# def kadane(MyList):
#     max_sum = 0
#     current_sum = 0
#     for i in MyList:
#         current_sum = current_sum + i
#         if current_sum < 0:
#             current_sum = 0
#         if max_sum < current_sum:
#             max_sum = current_sum
#     return max_sum
#
#
# # test the code
# MyList = [-3, 1, -8, 12, 0, -3, 5, -9, 4]
# print("Maximum SubArray is:", kadane(MyList))