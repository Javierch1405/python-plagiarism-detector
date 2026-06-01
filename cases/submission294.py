def check_length(text, limit):
    if len(text) <= limit:
        return "Valid"
    else:
        return "Too long"