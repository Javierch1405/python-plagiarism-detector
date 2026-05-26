def multiplication_table(num, limit):
    table = []
    for i in range(1, limit + 1):
        table.append(num * i)
    return table