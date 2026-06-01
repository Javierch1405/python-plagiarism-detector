def is_palindrome(text):
    clean_text = "".join(text.split()).lower()
    return clean_text == clean_text[::-1]