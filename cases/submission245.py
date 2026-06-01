def count_lines_with_keyword(lines_list, keyword):
    count = 0
    for line in lines_list:
        if keyword in line:
            count += 1
    return count