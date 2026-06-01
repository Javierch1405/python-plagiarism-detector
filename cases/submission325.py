def keep_vowels(text):
    vowels = "aeiouAEIOU"
    clean_str = ""
    for char in text:
        if char in vowels:
            clean_str += char
    return clean_str