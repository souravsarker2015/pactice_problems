def merge_array(a1, a2, n1, n2):
    i, j, k = 0, 0, 0
    a3 = [None] * (n1 + n2)
    while i < n1 and j < n2:
        if a1[i] < a2[j]:
            a3[k] = a1[i]
            i += 1
            k += 1
        else:
            a3[k] = a2[j]
            j += 1
            k += 1
    while i < n1:
        a3[k] = a1[i]
        i += 1
        k += 1
    while j < n2:
        a3[k] = a2[j]
        j += 1
        k += 1
    for i in range(n1 + n2):
        print(f"{a3[i]}", end=" ")


a1 = [1, 2, 3, 5, 6, 7, 8, 9]
a2 = [4, 5, 6, 8, 8, 99]
merge_array(a1, a2, len(a1), len(a2))

# def merge_array(arr1, arr2, n1, n2):
#     i, j, k = 0, 0, 0
#     arr3 = [None] * (n1 + n2)
#     while i < n1 and j < n2:
#         if arr1[i] < arr2[j]:
#             arr3[k] = arr1[i]
#             i += 1
#             k += 1
#         else:
#             arr3[k] = arr2[j]
#             j += 1
#             k += 1
#
#     while i < n1:
#         arr3[k] = arr1[i]
#         i += 1
#         k += 1
#     while j < n2:
#         arr3[k] = arr2[j]
#         j += 1
#         k += 1
#
#     for i in range(n1 + n2):
#         print(f"{arr3[i]}",end=" ")
#
#
# arr1 = [1, 2, 3, 5, 6, 8, 9]
# arr2 = [4, 7, 10, 11]
# n1 = len(arr1)
# n2 = len(arr2)
# merge_array(arr1, arr2, n1, n2)
