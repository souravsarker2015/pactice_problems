# def subarray_sum(arr):
#     current_sum = 0
#     max_sum = 0
#
#     for i in arr:
#         current_sum = current_sum + i
#         if current_sum < 0:
#             current_sum = 0
#         if max_sum < current_sum:
#             max_sum = current_sum
#     return max_sum
#
#
# arr = [1, 2, 3, 4, 5, 6, -11, 77]
# result = subarray_sum(arr)
# print(result)

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
        if max_sum < current_sum:
            max_sum = current_sum
            max_start = current_start
            max_end = current_end
    print(f"start from : {max_start}")
    print(f"end in : {max_end}")
    print(f"sum : {max_sum}")


arr = [1, 2, -15, 4, -6, -15, -1, ]
subarray_sum(arr)
