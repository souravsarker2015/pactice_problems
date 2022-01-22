lis = [1, 2, 3, 4, 4, 5, 6, 6, 7, 7]
# fre = [1, 2, 3, 4, 4, 5, 6, 6, 7, 7].count(7)
# print(fre)
print(lis)
# count = {}
# for i in lis:
#     if i in count:
#         count[i] += 1
#     else:
#         count[i] = 1
#
# print(count)

count = {}
for i in lis:
    if i in count:
        count[i] += 1
    else:
        count[i] = 1

print(count)
