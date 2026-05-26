def count_above_threshold(arr, threshold):
    count = 0
    for num in arr:
        if num > threshold:
            count += 1
    return count