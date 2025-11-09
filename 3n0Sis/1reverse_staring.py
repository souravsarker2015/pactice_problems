# n = input("Enter a sentence: ")
# n = n.split()
# # print(n)
# arr = []
# for i in n:
#     arr.append(i[::-1])
#
# print(arr)
# print(" ".join(arr))
#
# print(list(reversed(arr)))
# print(" ".join(list(reversed(arr))))

def reverse_string(n):
    n = n.split()
    arr = []
    for i in n:
        arr.append(i[::-1])
    print(" ".join(arr))
    print(arr)


n = input("Enter a string: ")
reverse_string(n)
