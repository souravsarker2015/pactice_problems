def frequencyArrayElement(arr):
    count = {}

    for i in arr:
        if i in count:
            count[i] += 1
        else:
            count[i] = 1
    return count


if __name__ == "__main__":
    array = [11, 33, 55, 11, 1, 2, 4]
    print(frequencyArrayElement(array))

