class QuickSort:
    def __init__(self, data):
        self.data = data

    def sort(self):
        self.quick_sort(0, len(self.data) - 1)

    def quick_sort(self, low, high):
        if low >= high:
            return

        pivot_index = self.partition(low, high)
        self.quick_sort(low, pivot_index - 1)
        self.quick_sort(pivot_index + 1, high)

    def partition(self, low, high):
        pivot_index = (low + high) // 2
        self.data[pivot_index], self.data[high] = self.data[high], self.data[pivot_index]

        for j in range(low, high):
            if self.data[j] <= self.data[high]:
                self.data[low], self.data[j] = self.data[j], self.data[low]
                low = low + 1

        self.data[low], self.data[high] = self.data[high], self.data[low]

        return low


if __name__ == "__main__":
    x = [2, 1, 4, 5, 7, 8, 15, 3]
    algo = QuickSort(x)
    algo.sort()
    print(x)
