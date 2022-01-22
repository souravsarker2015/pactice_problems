def power_of_two(n):
    if n == 0:
        return False

    while n != 1:
        if n % 2 != 0:
            return False
        n = n // 2
    return True


n = int(input("Enter the number : "))
result = power_of_two(n)
if result:
    print(f"{n} is power of two")

else:
    print(f"{n} is not power of two")
