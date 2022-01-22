a = {'1': 'apple',
     '2': 'mango',
     '3': 'pine-apple',
     '4': 'jack-fruit',
     '5': 'cucumber', }

for key, value in a.items():
    print(f"{key} : {value}")

for key in a:
    print(f"{key} : {a[key]}")
