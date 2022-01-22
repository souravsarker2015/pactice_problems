def subArray(arr):
    current_sum = 0
    maximum_sum = 0

    current_start = 0
    current_end = 0

    max_end = 0
    max_start = 0
    for i in range(len(arr)):
        current_sum = current_sum + arr[i]
        current_end = i

        if current_sum < 0:
            current_sum = 0
            current_start = current_end + 1

        if maximum_sum < current_sum:
            maximum_sum = current_sum
            max_start = current_start
            max_end = current_end

    print(maximum_sum)
    print(max_start)
    print(max_end)


if __name__ == "__main__":
    array = [1, 1, 2, 3, -65, 6, 9]
    subArray(array)
