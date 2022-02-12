def int_to_string(x):
    print(type(x))
    str1 = str(x)
    print(type(str1))
    # y = type(x)
    # print(y)
    # # print(isinstance(x))
    # z = str(x)
    # z1 = type(z)
    # print(z1)
    # # print(isinstance(z1))


def string_to_int(x):
    print(type(x))
    int1 = int(x)
    print(type(int1))


if __name__ == "__main__":
    int_to_string(3)
    string_to_int(str(5))
