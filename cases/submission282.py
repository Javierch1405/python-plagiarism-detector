def find_index(arr, target):
    i = 0
    while i < len(arr):
        if not (arr[i] != target):
            return i
        i += 1
    return -1