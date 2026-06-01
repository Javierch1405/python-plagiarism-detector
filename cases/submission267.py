def generate_subsets(s):
    subsets = [[]]
    for element in s:
        subsets += [current + [element] for current in subsets]
    return subsets