def classify_scores(scores):
    if not scores:
        return []
    results = []
    for score in scores:
        if score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        elif score >= 60:
            grade = "D"
        else:
            grade = "F"
        results.append(grade)
    return results

def main():
    scores = [95, 82, 73, 60, 88]
    grades = classify_scores(scores)
    for score, grade in zip(scores, grades):
        print(score, "->", grade)

main()
