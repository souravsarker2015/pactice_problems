employee = {
    1: 'Alice',
    2: 'john',
    3: 'jane',
    4: 'alice',
    5: 'bob'
}

files = {
    '100': 'jpeg',
    'Alice': 'png',
    '3': 'jpg',
    '1': 'jpg',
    'John': 'jpeg',

}

n = {}

for key, value in employee.items():
    print(f"{key}: {value}")
print()
for key, value in files.items():
    print(f"{key}: {value}")

# for key, value in files.items():
#     if value in n:
#         n[key] += 1
#     else:
#         n[key] = 1
print()
for i in files.values():
    # print(i)
    if i in n:
        n[i] += 1
    else:
        n[i] = 1

for key, value in n.items():
    print(f"{key} : {value}")  # from that we can get files unique value which has less value
    # min = 0.0000001
    #
    # if value < min:
    #     min = value
