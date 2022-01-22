def series_of_number(size):
    j = 9
    for i in range(1, size):
        if i > 0 and i <= 10:
            print(i, end=" ")
        else:
            print(j, end=" ")
            j -= 1


n = 20
series_of_number(n)
