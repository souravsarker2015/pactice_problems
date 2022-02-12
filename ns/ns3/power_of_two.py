def power_of_two(x):
    if x == 0:
        return False
    while x != 1:
        if x % 2 != 0:
            return False
        x = x // 2
    return True


n = int(input("enter a number : "))
res = power_of_two(n)
if res:
    print(f"{n} is power of two")

else:
    print(f"{n} is not power of two")
