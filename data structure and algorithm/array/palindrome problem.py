# n1 = 'baba'
# n2 = ""
# for i in range(len(n1) - 1, -1, -1):
#     n2 = n2 + n1[i]
# print(n2)
# if n1 == n2:
#     print('palindrome')
#
# else:
#     print('not palindrome')

# def isPalindrome(s):
#     data = list(s)
#     # print(data)
#     reverse_data = reverse(data)
#
#     if s == reverse_data:
#         return True
#     else:
#         return False
#
#
# def reverse(data):
#     start_index = 0
#     end_index = len(data) - 1
#     while end_index > start_index:
#         data[start_index], data[end_index] = data[end_index], data[start_index]
#         start_index += 1
#         end_index -= 1
#     # print(''.join(data))
#     return ''.join(data)


#
# if __name__ == '__main__':
#     st = 'amma'
#     result = isPalindrome(st)
#
#     if result:
#         print("Palindrome")
#     else:
#         print("Not Palindrome")


# n = 'radar'
#
# if n == n[::-1]:
#     print("palindrome")
# else:
#     print('Not Palindrome')

n = 'Madam'
n = n.casefold()

if n == n[::-1]:
    print("palindrome")
else:
    print("not palindrome")
