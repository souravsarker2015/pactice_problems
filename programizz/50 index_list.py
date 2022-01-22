li = [1, 2, 3, 4, 5, 6, 9]
lil = list(enumerate(li))

for index, value in lil:
    print(f"{index}  =  {value}")

for i in range(len(li)):
    print(f"{i} = {li[i]}")