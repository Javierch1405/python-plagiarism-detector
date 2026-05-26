def is_armstrong_number(num):
    num_str = str(num)
    power = len(num_str)
    total = sum(int(digit) ** power for digit in num_str)
    return total == num