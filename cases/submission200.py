def count_words(text):
    words = text.lower().split()
    frequencies = {}
    for word in words:
        if word in frequencies:
            frequencies[word] += 1
        else:
            frequencies[word] = 1
    return frequencies