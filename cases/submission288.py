def min_of_three(a, b, c):
    if b <= a and b <= c:
        return b
    elif a <= b and a <= c:
        return a
    else:
        return c