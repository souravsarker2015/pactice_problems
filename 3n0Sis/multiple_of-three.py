def multiple_of_three(l, h):
    count = 0
    print(f"Multiples of 3 between 1-200 in reversed order :")
    for i in range(h, l, -1):
        if i % 3 == 0:
            print(i, end=" ")
            count += 1

    print()
    print(f"Total counted: {count}")


multiple_of_three(1, 200)
