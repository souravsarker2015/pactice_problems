import math

data = [1, 2, 3, 4, 5]

startIndex = 0
endIndex = len(data) - 1
print(startIndex)
print(endIndex)

check_time = len(data) / 2
print(check_time)
for i in range(math.ceil(check_time)):
    if startIndex != endIndex:
        data[startIndex], data[endIndex] = data[endIndex], data[startIndex]
        startIndex += 1
        endIndex -= 1
# or
# while endIndex > startIndex:
#     data[startIndex], data[endIndex] = data[endIndex], data[startIndex]
#     startIndex += 1
#     endIndex -= 1

print(data)


