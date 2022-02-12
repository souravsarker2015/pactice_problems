def frequency(arr):
    count = {}
    for i in arr:
        if i in count:
            count[i] += 1
        else:
            count[i] = 1
    return count


if __name__ == "__main__":
    arr = [2, 4, 5, 6, 7, 4, 5, 7, 8, 8, 9]
    print(frequency(arr))
