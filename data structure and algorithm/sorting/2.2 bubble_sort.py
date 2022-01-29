class Bubble_Sort:
    def __init__(self, data):
        self.data = data

    def bubble_sort(self):
        length = len(self.data)
        for i in range(length - 1):
            swap = False
            for j in range(length - 1 - i):
                if self.data[j] > self.data[j + 1]:
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                    swap = True
            if not swap:
                break


if __name__ == "__main__":
    # ele = [2, 5, 7, 1, 9, 17, 6]
    ele = ['tuhin', 'hafiz', 'tito', 'anu']
    b = Bubble_Sort(ele)
    b.bubble_sort()
    print(ele)
