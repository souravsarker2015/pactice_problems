def selection_sort(arr):
    for i in range(len(arr) - 1):
        index = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[index]:
                index = j

        if index != i:
            arr[i], arr[index] = arr[index], arr[i]


if __name__ == "__main__":
    arr = [2, 3, 4, 52, 3]
    selection_sort(arr)
    print(arr)
