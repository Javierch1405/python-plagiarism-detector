def keep_vowels(text):
    vowels = "aeiouAEIOU"
    clean_str = ""
    for char in text:
        if char not in vowels:
            continue
        clean_str = clean_str + char
    return clean_str