class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        count = {}
        for i in s:
            count[i] = count.get(i, 0) + 1

        for i in t:
            if i not in count:
                return False
            count[i] -= 1
            if count[i] < 0:
                return False
        return all(value == 0 for value in count.values())


if __name__ == "__main__":
    sol = Solution()
    print(sol.isAnagram("anagram", "nagaram"))
