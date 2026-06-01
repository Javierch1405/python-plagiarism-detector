def make_zero_matrix(rows, cols):
    matrix = []
    for i in range(rows):
        row = [0] * cols
        matrix.append(row)
    return matrix