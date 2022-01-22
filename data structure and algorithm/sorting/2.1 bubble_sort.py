class Bubble_Sort:
    def __init__(self, arr):
        self.arr = arr

    def sort(self):
        for i in range(len(self.arr)):
            for j in range(len(self.arr) - i - 1):
                if self.arr[j] > self.arr[j + 1]:
                    self.swap(j, j + 1)

    def swap(self, i, j):
        self.arr[i], self.arr[j] = self.arr[j], self.arr[i]


if __name__ == "__main__":
    arr = [3, 2, 4, 6]
    bsort = Bubble_Sort(arr)
    bsort.sort()
    print(bsort.arr)
