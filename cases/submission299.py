def find_minimum(arr):
    lowest = arr[0]
    for i in range(1, len(arr)):
        if arr[i] < lowest:
            lowest = arr[i]
    return lowest