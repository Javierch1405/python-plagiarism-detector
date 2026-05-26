def detect_capital_use(word):
    if word.isupper():
        return True
    if word.islower():
        return True
    if word[0].isupper() and word[1:].islower():
        return True
    return False