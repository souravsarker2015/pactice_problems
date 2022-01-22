def insertion_sort(n):
    for i in range(len(n)):
        j = i
        while j > 0 and n[j - 1] > n[j]:
            n[j - 1], n[j] = n[j], n[j - 1]
            j = j - 1


if __name__ == "__main__":
    n = [1, 6, 3, 6, 8, 89, 2]
    insertion_sort(n)
    print(n)
