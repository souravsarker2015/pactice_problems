l1 = [1, 2, 3]
l2 = ['a', 'app', 'apple']

dic_two = dict(zip(l1, l2))
print(dic_two)

dictionary = {k: v for k, v in zip(l1, l2)}
print(dictionary)
