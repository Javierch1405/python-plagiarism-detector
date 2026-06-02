def compute_average(nums):
    if not nums:
        return 0
    return sum(nums) / len(nums)


if __name__ == "__main__":
    import sys
    data = list(map(int, sys.stdin.read().split())) or [1, 2, 3]
    print(compute_average(data))
