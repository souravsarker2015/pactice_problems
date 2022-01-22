class QuickSort:
    def __init__(self, arr):
        self.arr = arr

    def sort(self):
        return self.quicksort(0, len(self.arr) - 1)

    def quicksort(self, low, high):
        if low >= high:
            return

        pivot = self.partition(low, high)
        self.quicksort(low, pivot - 1)
        self.quicksort(pivot + 1, high)

    def partition(self, low, high):
        pivot = (low + high) // 2
        self.arr[pivot], self.arr[high] = self.arr[high], self.arr[pivot]

        for j in range(low, high):
            if self.arr[j] < self.arr[high]:
                self.arr[j], self.arr[low] = self.arr[low], self.arr[j]
                low += 1
        self.arr[low], self.arr[high] = self.arr[high], self.arr[low]
        return low


if __name__ == "__main__":
    arr = [3, 5, 1, 3, 2]
    qsort = QuickSort(arr)
    qsort.sort()
    print(arr)
