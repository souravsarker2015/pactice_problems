# def subarray(arr):
#     current_sum = 0
#     maximum_sum = 0
#
#     current_start = 0
#     current_end = 0
#
#     max_start = 0
#     max_end = 0
#     for i in range(len(arr)):
#         current_sum = current_sum + arr[i]
#         current_end = i
#         if current_sum < 0:
#             current_sum = 0
#             current_start = current_end + 1
#         if maximum_sum < current_sum:
#             maximum_sum = current_sum
#             max_start = current_start
#             max_end = current_end
#
#     print(maximum_sum)
#     print(max_start)
#     print(max_end)
#
#
# arr = [-1, -6, -7, 3, 6, 1]
# subarray(arr)


def subarray(arr):
    current_sum = 0
    maximum_sum = 0

    current_start = 0
    current_end = 0

    maximum_start = 0
    maximum_end = 0

    for i in range(len(arr)):
        current_end = i
        current_sum = current_sum + arr[i]
        if current_sum < 0:
            current_sum = 0
            current_start = current_end + 1
        if maximum_sum < current_sum:
            maximum_sum = current_sum
            maximum_start = current_start
            maximum_end = current_end
    print(maximum_start)
    print(maximum_end)
    print(maximum_sum)


if __name__ == "__main__":
    arr = [1, -2, 5, 7, 15]
    subarray(arr)
