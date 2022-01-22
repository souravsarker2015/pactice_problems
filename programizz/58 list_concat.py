# l1 = ['a', 'b', 2, 5, 'cat']
# l2=list(range(5,10))
# print(l1+l2)
# l1.extend(l2)
# print(l1)

n1 = 'This a laptop'
n2 = n1.split()
temp=[]
for i in n2:
    temp.append(i[::-1])

print(temp)
print(" ".join(temp))
print(" ".join(list(reversed(temp))))
