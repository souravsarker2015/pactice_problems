def matrix_transpose(a):
    c = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]

    for i in range(len(a)):
        for j in range(len(a[0])):
            c[j][i] = a[i][j]

    for i in c:
        print(i)


if __name__ == "__main__":
    a = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]

    # b = [[1, 2, 3],
    #      [4, 5, 6],
    #      [7, 8, 9]]
    matrix_transpose(a)
