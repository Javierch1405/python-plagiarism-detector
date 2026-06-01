def get_grade(score):
    if score < 70:
        return "F"
    if score < 80:
        return "C"
    if score < 90:
        return "B"
    return "A"