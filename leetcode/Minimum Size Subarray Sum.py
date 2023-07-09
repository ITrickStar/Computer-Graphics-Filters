# Minimum Size Subarray Sum

import numpy as np


class Solution(object):
    def minSubArrayLen(self, target, nums):
        """
        :type target: int
        :type nums: List[int]
        :rtype: int
        """

        def list_sum(nums: list) -> int:
            sum = 0
            for i in nums:
                sum += i
            return sum

        if (list_sum(nums) < target):
            return 0
        minsize = len(nums)
        start = 0
        end = 1

        while end < len(nums)+1:
            tmp = nums[start:end]
            sum = list_sum(tmp)
            if sum < target:
                end += 1
            else:
                if (len(tmp) < minsize):
                    minsize = len(tmp)
                start += 1

        return minsize


if __name__ == "__main__":
    nums = [1, 1, 2, 2]
    target = 4
    sol = Solution()
    print(sol. minSubArrayLen(target, nums))
