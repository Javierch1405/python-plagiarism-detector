def find_max(arr):
    if not arr:
        return None
    max_val = arr[0]
    for element in arr:
        if element > max_val:
            max_val = element
    return max_val