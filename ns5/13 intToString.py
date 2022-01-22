def intToString(a):
    a = int(a)
    print(type(a))
    print(a)

    st = str(a)
    print(type(st))
    print(st)


def stringToInt(s):
    print(s)
    print(type(s))
    a = int(s)
    print(type(a))
    print(a)


if __name__ == "__main__":
    st = '123'
    a = 123
    intToString(a)
    stringToInt(st)
