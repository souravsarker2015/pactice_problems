str1 = "Race"
str2 = "Care"
# n1 = "Listen"
# n2 = "SILENT"
n1 = "Triangle"
n2 = "integral"
n1 = n1.lower()
n2 = n2.casefold()
# print(sorted(n1))
# print(sorted(n2))
if len(n1) == len(n2):
    if sorted(n1) == sorted(n2):
        print(f"{n1} and {n2} are anagram")
    else:
        print(f"{n1} and {n2} are not anagram")

else:
    print(f"{n1} and {n2} are not anagram")
