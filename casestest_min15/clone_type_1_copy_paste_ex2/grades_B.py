def classify_scores(scores):
    # asigna una letra a cada calificacion
    results=[]
    for score in scores:
        if score>=90:
            grade='A'
        elif score>=80:
            grade='B'
        elif score>=70:
            grade='C'
        else:
            grade='F'
        results.append(grade)
    return results


def main():
    scores=[95,82,73,60,88]
    grades=classify_scores(scores)
    for score,grade in zip(scores,grades):
        print(score,'->',grade)


main()
