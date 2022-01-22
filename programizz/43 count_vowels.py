vowels = 'aeiou'
n = 'Hello, have you tried our tutorial section yet?'
n = n.casefold()
count = {}.fromkeys(vowels, 0)
for i in n:
    if i in count:
        count[i] += 1
    # else:
    #     count[i]=1

print(count)
# for key, value in count.items():
#     print(f"{key} : {value}")
