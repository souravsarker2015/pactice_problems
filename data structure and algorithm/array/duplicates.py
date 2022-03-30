# def duplicate(arr):
#     # n = len(arr)
#     temp = []
#
#     for i in range(len(arr)):
#         for j in range(i + 1, len(arr)):
#             if arr[i] == arr[j] and arr[i] not in temp:
#                 temp.append(arr[i])
#     return temp


# # TC= O(N^2)
# arr = [11, 11, 1, 23, 5, 6, 45, 6, 5, 5, 4, 5]
# print(duplicate(arr))

def duplicate_value(arr):
    for i in arr:
        if arr[abs(i)] >= 0:
            arr[abs(i)] = -arr[abs(i)]
        else:
            print(f"{abs(i)}")


arr = [1, 1, 2, 5, 8]
duplicate_value(arr)
