def run_length_encoding(text):
    if not text:
        return ""
    encoded = ""
    current_char = text[0]
    count = 1
    for char in text[1:]:
        if char == current_char:
            count += 1
        else:
            encoded += current_char + str(count)
            current_char = char
            count = 1
    encoded += current_char + str(count)
    return encoded