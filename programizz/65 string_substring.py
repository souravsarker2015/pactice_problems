n = 'I love bangladesh'

print(n[:])
print(n[1:])
print(n[:-1])
print(n[-1:])
print(n[::-1])

temp = []
n = n.split()
print(n)
for i in n:
    temp.append(i)
print(temp)
a = []
print(n[::-1])

for i in range(len(n) - 1, -1, -1):
    a.append(n[i])
print(" ".join(a))



# # print each statement on a new line
# print("Python")
# print("is easy to learn.")
#
# # new line
# print()
#
# # print both the statements on a single line
# print("Python", end=" ")
# print("is easy to learn.")