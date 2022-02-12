def frequency(arr):
    count = {}

    for i in arr:
        if i in count:
            count[i] += 1
        else:
            count[i] = 1

    return count


if __name__ == "__main__":
    arr = [11, 22, 33, 11, 22]
    print(frequency(arr))
