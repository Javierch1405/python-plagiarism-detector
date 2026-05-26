def sum_list(items):
    total = 0
    idx = 0
    while idx < len(items):
        total = total + items[idx]
        idx = idx + 1
    return total