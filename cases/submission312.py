def has_negative(arr):
    result = any(not (x >= 0) for x in arr)
    return result