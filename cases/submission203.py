def remove_duplicates(arr):
    unique_list = []
    for item in arr:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list