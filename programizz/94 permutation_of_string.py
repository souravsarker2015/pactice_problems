def permutation(words, i=0):
    if i == len(words):
        print("".join(words))

    for j in range(i, len(words)):
        words = [c for c in words]
        words[i], words[j] = words[j], words[i]
        permutation(words, i=i + 1)


permutation('abc')

# from itertools import permutations
#
# words=[" ".join(p) for p in permutations('pro')]
# print(words)