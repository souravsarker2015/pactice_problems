def selection_sort(array):
    for i in range(len(array) - 1):
        index = i
        for j in range(i+1, len(array)):
            if array[j] < array[index]:
                index = j

        if index != i:
            array[index], array[i] = array[i], array[index]


array = [5, 6, 3, 1, 2]
selection_sort(array)
print(array)

# def selection_sort(n):
#     for i in range(len(n) - 1):
#         index = i
#         for j in range(i, len(n)):
#             if n[j] < n[index]:
#                 index = j
#         if index != i:
#             n[index], n[i] = n[i], n[index]
#
#
# if __name__ == "__main__":
#     n = [1, 5, 15, 6, 8, 9]
#     selection_sort(n)
#     print(n)
