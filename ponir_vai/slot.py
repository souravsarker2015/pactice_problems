slots = [
    {
        'slot_id': 12345,
        'users': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    },
    {
        'slot_id': 12346,
        'users': [50, 51, 52, 53, 54, 55]
    },
    {
        'slot_id': 12347,
        'users': [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
    },
    {
        'slot_id': 12348,
        'users': [26, 27, 28]
    },
    {
        'slot_id': 12349,
        'users': [29, 30]
    },
    {
        'slot_id': 12350,
        'users': [46, 47]
    },
    {
        'slot_id': 12351,
        'users': [48, 49]
    },
    {
        'slot_id': 12352,
        'users': [31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45]
    },
]

total_user = []
for slot in slots:
    user = slot.get('users')
    total_user = total_user + user


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


run_data = []


def make_slot(data, s):
    print('data', data)
    slot_data = []
    slot_data.append({
        "slot_id": s,
        "users": data
    })
    return slot_data


r = []
arr1 = []
slot_id_list = []
for slot in slots:
    length = len(slot.get('users'))

    if length <= 4:
        arr1 = arr1 + slot.get('users')
        slot_id_list.append(slot.get('slot_id'))

    if 4 < length < 10:
        print('individual')
        run_data.append({
            "id": "run#1",
            "type": "individual",
            "slots": slot.get('slot_id'),
            "users": slot.get('users'),
            "waiting_list": [],
            "pairs": []
        })

    if length >= 10:
        n = 5
        x = list(divide_chunks(slot.get('users'), n))
        run = 1
        slot_id = slot.get('slot_id')
        for i in x:
            run = run + 1
            run_data.append({
                "id": f"run#{run}",
                "type": "split",
                "slots": make_slot(i, slot_id),
                "waiting_list": [],
                "pairs": []
            })


def merge_data(arr1, slot_id_list):
    n = 5
    merge_arr_list = list(divide_chunks(arr1, n))
    list_data_all = []
    for j in merge_arr_list:
        list_data_all = list_data_all + j
    run_data.append({
        "id": "run#1",
        "type": "merged",
        "slots": slot_id_list,
        "users": list_data_all,
        "waiting_list": [],
        "pairs": []
    })


merge_data(arr1, slot_id_list)

json_data = {
    "room": "room#1",
    "rsvp_users": total_user,
    "runs": run_data
}
print('json_data', json_data)

# json_data = {
#     "room": "room#1",
#     "rsvp_users": [1, 2, 3, 5, 6, 7]
#     "runs": [
#         {
#             "id": "run#1",
#             "type": "individual",
#             "slots": 13445,
#             "users": []
#             "waiting_list": [],
#             "pairs": []
#         },
#         {
#             "id": "run#1",
#             "type": "merged",
#             "slots": [12345, 12346, 12367],
#             "users": [],
#             "waiting_list": [],
#             "pairs": []
#         },
#         {
#             "id": "run#1",
#             "type": "split",
#             "users": [],
#             "slots": [
#                 {
#                     "slot_id": 13345,
#                     "users": [1, 2, 3, 4, 5]
#                 }
#             ],
#             "waiting_list": [],
#             "pairs": []
#         },
#         {
#             "id": "run#1",
#             "type": "split",
#             "users": [],
#             "slots": [
#                 {
#                     "slot_id": 13345,
#                     "users": [1, 2, 3, 4, 5]
#                 }
#             ],
#             "waiting_list": [],
#             "pairs": []
#         },
#     ]
# }
