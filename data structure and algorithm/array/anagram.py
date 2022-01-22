def anagram(n1, n2):
    n1 = n1.casefold()
    n2 = n2.casefold()
    n1 = sorted(list(n1))
    n2 = sorted(list(n2))

    if len(n1) == len(n2):
        if n1 == n2:
            return True
        else:
            return False
    else:
        return False


n1 = 'race'
n2 = 'care'

result = anagram(n1, n2)
if result:
    print(print('anagram'))
else:
    print("not anagram")

# n = 'I Love Bangladesh'
# arr=[]
# for i in n:
#     arr.append(i)
#
# print(arr)
