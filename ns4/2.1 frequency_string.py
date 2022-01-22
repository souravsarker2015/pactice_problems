# st = "I Love Bangladesh l,s i,o"
#
# st = st.casefold()
#
# count = {}
# for i in st:
#     if i in count:
#         count[i] += 1
#     else:
#         count[i] = 1
#
# print(count)

st = "I Love Bangladesh"
st = st.split()
temp = []
for i in st:
    temp.append(i[::-1])
print(" ".join(temp))

# st = list(reversed(st))
# for i in range(len(st) - 1, -1, -1):
#     print(st[i], end=" ")

# print(st[::-1])
# print(st)
