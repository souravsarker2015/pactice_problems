# x = [[1, 2, 3],
#      [1, 2, 3],
#      [1, 2, 3]]
#
# y = [[1, 2, 3],
#      [1, 2, 3],
#      [1, 2, 3]]
#
# res = [[0, 0, 0],
#        [0, 0, 0],
#        [0, 0, 0]]
#
# for i in range(len(x)):
#     for j in range(len(y[0])):
#         for k in range(len(y)):
#             res[i][j] = x[i][k] * y[k][j]
#
# for r in res:
#     print(r)

def multiplication(x, y):
    res = [[0, 0, 0],
           [0, 0, 0],
           [0, 0, 0]]
    for i in range(len(x)):
        for j in range(len(y[0])):
            for k in range(len(y)):
                res[i][j] = x[i][k] * y[k][j]
    for r in res:
        print(r)


x = [[1, 2, 3],
     [1, 2, 3],
     [1, 2, 3]]

y = [[1, 2, 3],
     [1, 2, 3],
     [1, 2, 3]]

multiplication(x, y)
