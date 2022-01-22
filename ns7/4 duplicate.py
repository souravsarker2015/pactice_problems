def duplicate(arr):
    temp = []
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j] and arr[i] not in temp:
                temp.append(arr[i])

    return temp


if __name__ == "__main__":
    arr = [1, 2, 1, 3, 2, 5, 6, 7, 7]
    print(duplicate(arr))
