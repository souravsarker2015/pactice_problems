class InsertionSort:
    def __init__(self, data):
        self.data = data

    def insertion_sort(self):
        for i in range(1, len(self.data)):
            j = i
            while j > 0 and self.data[j - 1] > self.data[j]:
                self.data[j - 1], self.data[j] = self.data[j], self.data[j - 1]
                j -= 1


if __name__ == "__main__":
    el = [1, 6, 3, 2, 9, 5]
    i = InsertionSort(el)
    i.insertion_sort()
    print(el)
