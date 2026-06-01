def first_seven_multiplier(arr):
    for num in arr:
        if num % 7 == 0:
            return num
    return None