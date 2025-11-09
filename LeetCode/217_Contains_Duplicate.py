from typing import List


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False


if __name__ == "__main__":
    sol = Solution()
    test_cases = [[1, 2, 3, 4], [1, 2, 3, 1]]
    for case in test_cases:
        print(f"containsDuplicate({case}) = {sol.containsDuplicate(case)}")
