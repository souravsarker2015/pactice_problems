import random

lis = [1, 2, 3, 'a', 'aaap']
res = random.choice(lis)
print(res)


# isFloat

def isFloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


print(isFloat(12.56))
print(isFloat('dhsg'))
