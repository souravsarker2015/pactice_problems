a = {2: 2,
     1: 1,
     3: 3,
     4: 4,
     5: 5, }

a_key, a_value = sorted(a.keys()), sorted(a.values())
# print(f"{a_key} : {a_value}")
for key in sorted(a.keys()):
    print(f"{key} ")

a_sorted = {key: value for key, value in sorted(a.items(), key=lambda item: item[1])}
print(a_sorted)

if 2 in a:
    print("Present")