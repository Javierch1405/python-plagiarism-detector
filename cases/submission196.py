def is_anagram(str1, str2):
    clean1 = str1.lower().replace(" ", "")
    clean2 = str2.lower().replace(" ", "")
    return sorted(clean1) == sorted(clean2)