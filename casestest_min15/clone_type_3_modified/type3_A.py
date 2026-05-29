def compute_stats(numbers):
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
    return mean, variance

def main():
    data = [4, 8, 15, 16, 23, 42]
    mean, variance = compute_stats(data)
    print("mean:", mean)
    print("variance:", variance)

main()
