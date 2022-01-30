class SelectionSort:
    def __init__(self, data):
        self.data = data

    def selection_sort(self):
        length = len(self.data)
        for i in range(length - 1):
            min = i
            for j in range(i+1, length):
                if self.data[j] < self.data[min]:
                    min = j

            if i != min:
                self.data[min], self.data[i] = self.data[i], self.data[min]


if __name__ == "__main__":
    ele = [1, 6, 2, 4, 3, 9, 8]
    s = SelectionSort(ele)
    s.selection_sort()
    print(ele)
