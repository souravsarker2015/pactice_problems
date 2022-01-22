class QuickSort:
    def __init__(self, data):
        self.data = data

    def sort(self):
        self.quickSort(0, len(self.data)-1)

    def quickSort(self, low, high):
        if low >= high:
            return

        pivot = self.partition(low, high)
        self.quickSort(low, pivot - 1)
        self.quickSort(pivot + 1, high)

    def partition(self, low, high):
        pivot_index = (high + low) // 2

        self.data[pivot_index], self.data[high] = self.data[high], self.data[pivot_index]

        for i in range(low, high):
            if self.data[i] <= self.data[high]:
                self.data[low], self.data[i] = self.data[i], self.data[low]
                low = low + 1
        self.data[low], self.data[high] = self.data[high], self.data[low]
        return low


if __name__ == "__main__":
    n = [2, 1, 4, 3]
    quick = QuickSort(n)
    quick.sort()
    print(n)
