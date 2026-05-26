def find_minimum(arr):
    lowest = arr[0]
    for element in arr:
        if not (element >= lowest):
            lowest = element
    return lowest