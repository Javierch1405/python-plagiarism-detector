def find_mode(arr):
    if not arr:
        return None
    frequencies = {}
    for item in arr:
        frequencies[item] = frequencies.get(item, 0) + 1
    max_count = max(frequencies.values())
    modes = [k for k, v in frequencies.items() if v == max_count]
    return modes[0]