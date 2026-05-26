def contains_substring(main_str, sub_str):
    if not sub_str:
        return True
    for i in range(len(main_str) - len(sub_str) + 1):
        if main_str[i:i+len(sub_str)] == sub_str:
            return True
    return False