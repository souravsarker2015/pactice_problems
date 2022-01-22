# n = int(input("Enter a range :"))
#
# n1, n2 = 0, 1
#
# for i in range(2, n + 1):
#     print(n1, end=" ")
#     n3 = n1 + n2
#     n1 = n2
#     n2 = n3


def rec_fibo(n):
    if n <= 1:
        return n
    else:
        return rec_fibo(n - 1) + rec_fibo(n - 2)


if __name__ == "__main__":
    n = int(input("Enter a Range : "))

    if n <= 0:
        print("Enter a positive number")

    else:
        for i in range(n + 1):
            print(rec_fibo(i), end=" ")
