def filter_long_words(words, min_len):
    long_words = []
    for w in words:
        if len(w) >= min_len:
            long_words.append(w)
    return long_words