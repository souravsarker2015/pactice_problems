def matrix_sum(a, b):
    c = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]

    for i in range(len(a)):
        for j in range(len(b[0])):
            c[i][j] = a[i][j] + b[i][j]

    for i in c:
        print(i)


if __name__ == "__main__":
    a = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]

    b = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]
    matrix_sum(a, b)
