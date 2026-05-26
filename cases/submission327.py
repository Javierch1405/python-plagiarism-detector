def flatten_coordinates(matrix):
    coords = []
    for r in range(len(matrix)):
        for c in range(len(matrix[r])):
            coords.append((r, c))
    return coords