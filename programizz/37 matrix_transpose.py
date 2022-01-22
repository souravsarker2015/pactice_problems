y = [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]

res = [[0, 0, 0],
       [0, 0, 0],
       [0, 0, 0]]

for i in range(len(y)):
    for j in range(len(y[0])):
        res[j][i]=y[i][j]

for r in res:
    print(r)