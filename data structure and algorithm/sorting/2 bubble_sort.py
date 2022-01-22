class BubbleSort:
    def __init__(self, nums):
        self.nums = nums

    def sort(self):
        for i in range(len(self.nums) - 1):
            for j in range(len(self.nums) - i - 1):
                if self.nums[j] > self.nums[j+1]:
                    self.swap(j, j + 1)

    def swap(self, i, j):
        self.nums[i], self.nums[j] = self.nums[j], self.nums[i]


if __name__ == "__main__":
    n = [-55, -9, -15, 15, 78, 2, 6, 1, 89]
    bubble_sort = BubbleSort(n)
    bubble_sort.sort()
    print(bubble_sort.nums)
