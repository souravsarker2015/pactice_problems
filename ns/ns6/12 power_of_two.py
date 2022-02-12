def power_of_two(x):
    if x == 0:
        return False

    while x != 1:
        if x % 2 != 0:
            return False
        x = x / 2
    return True


if __name__ == "__main__":
    x = int(input("Enter a Number : "))

    result = power_of_two(x)
    if result:
        print(f"{x} is power of two")
    else:
        print(f"{x} is not power of two")
