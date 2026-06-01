def flatten_coordinates(matrix):
    coords = []
    for c in range(len(matrix[0]) if matrix else 0):
        for r in range(len(matrix)):
            coords.insert(len(coords), (r, c))
    # Note: Sorted to maintain identical functional output despite logic flow alteration
    return sorted(coords, key=lambda x: (x[0], x[1]))