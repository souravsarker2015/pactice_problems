def powerOfTwo(n):
    if n == 0:
        return False

    while n != 1:
        if n % 2 != 0:
            return False
        n = n // 2
    return True


if __name__ == "__main__":
    n = 6
    res = powerOfTwo(n)
    if res:
        print(f"{n} is power of two")

    else:
        print(f"{n} is not power of two")
