# str = "car car"
# char = 'c'
# count = 0
# for i in str:
#     if i == char:
#         count += 1
#
# print(count)

str = "car car"

count = {}

for i in str:
    if i in count:
        count[i] += 1
    else:
        count[i] = 1
print(count)