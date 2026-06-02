def compute_average(nums):
    total = 0
    count = 0
    for n in nums:
        total += n
        count += 1
    return total / count if count else 0


if __name__ == "__main__":
    import sys
    data = [int(x) for x in sys.stdin.read().split()] or [1, 2, 3]
    print(compute_average(data))
