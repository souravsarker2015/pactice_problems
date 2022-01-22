def insertion_sort(arr):
    for i in range(len(arr)):
        j = i
        while j > 0 and arr[j - 1] > arr[j]:
            arr[j - 1], arr[j] = arr[j], arr[j - 1]
            j -= 1


if __name__ == "__main__":
    arr = [1, 5, 3, 8, 7]
    insertion_sort(arr)
    print(arr)
