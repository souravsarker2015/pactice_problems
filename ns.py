
############################################################
# function for kadane's algorithm
# def kadane(MyList):
#     max_sum = 0
#     current_sum = 0
#
#     max_start = 0
#     max_end = 0
#     current_start = 0
#     current_end = 0
#
#     for i in range(len(MyList)):
#         current_sum = current_sum + MyList[i]
#         current_end = i
#         if current_sum < 0:
#             current_sum = 0
#             # Start a new sequence from next element
#             current_start = current_end + 1
#
#         if max_sum < current_sum:
#             max_sum = current_sum
#             max_start = current_start
#             max_end = current_end
#
#     print("Maximum SubArray is:", max_sum)
#     print("Start index of max_Sum:", max_start)
#     print("End index of max_Sum:", max_end)
#
#
# # test the code
# MyList = [-3, 1, -8, 12, 0, -3, 5, -9, 4]
# kadane(MyList)

# maximum subarray
# def subarray(arr):
#     max_sum = 0
#     current_sum = 0
#     for i in arr:
#         current_sum = current_sum + i
#         if current_sum < 0:
#             current_sum = 0
#         if max_sum < current_sum:
#             max_sum = current_sum
#     return max_sum
#
#
# arr = [-3, 1, -8, 12, 0, -3, 5, -9, 4]
# print("maximum subarray is: ", subarray(arr))

################################################################
# Calculating n-th real root using binary search
# def find_root(x, n):
#     x = float(x)
#     n = int(n)
#
#     if x >= 0 and x <= 1:
#         high = 1
#         low = x
#     else:
#         high = x
#         low = 1
#
#     epsilon = 0.00000001
#     guess = (high + low) / 2
#
#     while abs(guess ** n - x) >= epsilon:
#         if guess ** n > x:
#             high = guess
#         else:
#             low = guess
#         guess = (high + low) / 2
#     print(guess)
#
#
# x = 5
# n = 2
# find_root(x, n)

# binary search on sorted rotated array
# def search(arr, l, h, n):
#     if l > h:
#         return -1
#     mid = (l + h) // 2
#     if arr[mid] == n:
#         return mid
#
#     if arr[l] <= arr[mid]:
#         if n >= arr[l] and n <= arr[mid]:
#             return search(arr, l, mid - 1, n)
#         return search(arr, mid + 1, h - 1, n)
#
#     if n >= arr[mid] and n <= arr[h]:
#         return search(arr, mid + 1, h, n)
#     return search(arr, l, mid - 1, n)
#
# arr = [4, 5, 6, 7, 8, 9, 1, 2, 3]
# n = 1
# result = search(arr, 0, len(arr) - 1, n)
#
# if result != -1:
#     print("index : ", result)
# else:
#     print("not found")


##################################################################

# def binary_search(arr, l, r, x):
#     if r >= l:
#         mid = l + (r - l) // 2
#         if arr[mid] == x:
#             return mid
#
#         elif arr[mid] > x:
#             return binary_search(arr, l, mid - 1, x)
#         else:
#             return binary_search(arr, mid + 1, r, x)
#
#     else:
#         return -1
#
#
# arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# x = 10
# result = binary_search(arr, 0, len(arr) - 1, x)
#
# if result != -1:
#     print("Element is present in %d" % result)
# else:
#     print("Element is not present in list", )
###################################################


######################################################################

# common elements among 2/3 sorted array. Using only loop
# def common_element(a1, a2, a3, n1, n2, n3):
#     i, j, k = 0, 0, 0
#
#     while i < n1 and j < n2 and k < n3:
#         if a1[i] == a2[j] and a2[j] == a3[k]:
#             print(a1[i])
#             i += 1
#             j += 1
#             k += 1
#
#         elif a1[i] < a2[j]:
#             i += 1
#         elif a2[j] < a3[k]:
#             j += 1
#         else:
#             k += 1
#
#
# arr1 = [1, 2, 3, 4, 5, 6, 7, 9, 6, 3, 4, 6]
# arr2 = [2, 3, 4, 6, 4, 8, 2, 2, 3, 3, 5, 4]
# arr3 = [1, 1, 2, 5, 4, 2, 3, 5, 6, 6, 2, 3, 6]
# n1 = len(arr1)
# n2 = len(arr2)
# n3 = len(arr3)
# common_element(arr1, arr2, arr3, n1, n2, n3)

#########################################################################

# int to string and string to int conversion
# n = "123"
# z = int(n)
# print(type(z))
# print(z)
# n1 = str(z)
# print(type(n1))
# print(n1)

######################################################################

# Power of two
# def power_of_two(n):
#     if n == 0:
#         return False
#     while n != 1:
#         if n % 2 != 0:
#             return False
#         n = n // 2
#     return True
#
#
# n = int(input("Enter the Number :"))
# if power_of_two(n):
#     print(f"{n} is power of two")
# else:
#     print(f"{n} is not power of two")

###############################################################################

# max and min
# list1 = [1, 2, 3, 4, 5, 6, 7, 4, 3, 3, 46, 8, 8, 8]
# n = len(list1)
# maximum = list1[0]
# minimum = list1[0]
# for i in range(n):
#     if list1[i] < minimum:
#         minimum = list1[i]
# print(f"Minimum element of the list : {minimum}")
#
# for i in range(n):
#     if list1[i] > maximum:
#         maximum = list1[i]
# print(f"Maximum element of the list : {maximum}")
#
# l = list(map(int, input("enter the elements: ").strip().split(" ")))
# print(l)

##########################################################################

# Find all missing elements
# def missing(arr):
#     n = len(arr)
#     d = arr[0]
#
#     for i in range(n):
#         if (arr[i] - i != d):
#             while d < arr[i] - i:
#                 print(i + d, end=" ")
#                 d += 1
#
#
# arr = [1, 2, 5, 6, 10]
# missing(arr)

######################################################################

# # duplicate value find
# def repeated(arr):
#     n = len(arr)
#     arr1=[]
#     for i in range(n):
#         k=i+1
#         for j in range(k,n):
#             if arr[i]==arr[j] and arr[i] not in arr1:
#                 arr1.append(arr[i])
#     print("Duplicate Values in List : ")
#     print(f"{arr1}", end=" ")
#
#
# arr = [1, 2, 54, 1, 5, 1, 3, 5, 4, 2, 1, 5, 4, 1, 1, 5, 1, 5, 1]
# repeated(arr)

######################################################################

# merge two sorted array

# def array_merge(a1, a2, n1, n2):
#     a3 = [None] * (n1 + n2)
#     i = 0
#     j = 0
#     k = 0
#
#     # arr1 = [4, 8, 10, 15, 26] 5
#     # arr2 = [6, 8, 9, 45, 66] 5
#     while i < n1 and j < n2:
#         if a1[i] < a2[j]:
#             a3[k] = a1[i]
#             i += 1
#             k += 1
#
#         else:
#             a3[k] = a2[j]
#             j += 1
#             k += 1
#
#     while i < n1:
#         a3[k] = a1[i]
#         i += 1
#         k += 1
#
#     while j < n2:
#         a3[k] = a2[j]
#         j += 1
#         k += 1
#     print("Merged Array: ")
#     for i in range(n1 + n2):
#         print(str(a3[i]), end=" ")
#
#
# arr1 = [4, 8, 10, 15, 26]
# n1 = len(arr1)
# print(n1)
# arr2 = [6, 8, 9, 45, 66]
# n2 = len(arr2)
# print(n2)
# array_merge(arr1, arr2, n1, n2)

#############################################################################

# counting the frequency of array elements

# arr = [10, 12, 13, 15, 10, 12, 15, 13, 6, 8, 0]
#
# count = {}
#
# for i in arr:
#     if i in count:
#         count[i] += 1
#     else:
#         count[i] = 1
#
# for key, value in count.items():
#     print(f"{key} : {value}")
