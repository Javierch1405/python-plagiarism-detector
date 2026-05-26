def contains_item(lst, item):
    found = False
    i = 0
    while i < len(lst):
        if lst[i] == item:
            found = True
            break
        i += 1
    return found