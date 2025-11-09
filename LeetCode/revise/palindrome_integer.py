class Solution:
    def isPalindrome(self, x: int) -> bool:
        pass


if __name__ == "__main__":
    sol = Solution()
    test_cases = [121, -121, 10, 12321, 0]
    for case in test_cases:
        print(f"isPalindrome({case}) = {sol.isPalindrome(case)}")
