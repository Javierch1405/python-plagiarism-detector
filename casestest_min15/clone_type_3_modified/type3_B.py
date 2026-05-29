import math

def compute_stats(numbers):
    if not numbers:
        return 0, 0
    total = 0
    count = 0
    for value in numbers:
        total += value
        count += 1
    mean = total / count
    variance = 0
    for value in numbers:
        diff = value - mean
        variance += diff * diff
    variance = variance / count
    stddev = math.sqrt(variance)
    return mean, stddev

def main():
    data = [4, 8, 15, 16, 23, 42]
    mean, stddev = compute_stats(data)
    print("mean:", mean)
    print("stddev:", stddev)

main()
