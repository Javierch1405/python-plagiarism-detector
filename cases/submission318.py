def filter_long_words(words, min_len):
    return [w for w in words if not (len(w) < min_len)]