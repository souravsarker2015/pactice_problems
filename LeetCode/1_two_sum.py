from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        new_dict = {}
        for i, num in enumerate(nums):
            component = target - num
            if component in new_dict:
                return [new_dict[component], i]
            new_dict[num] = i
        return []


if __name__ == "__main__":
    sol = Solution()
    test_cases = [[2, 7, 11, 15], [3, 2, 4], [3, 3]]
    for case in test_cases:
        print(f"twoSum({case}, 9) = {sol.twoSum(case, 9)}")
