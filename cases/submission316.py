def first_seven_multiplier(arr):
    match = None
    idx = 0
    while idx < len(arr):
        if arr[idx] % 7 == 0:
            match = arr[idx]
            break
        idx += 1
    return match