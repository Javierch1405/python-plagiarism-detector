def is_perfect_number(num):
    if num <= 1:
        return False
    total = 0
    for i in range(1, num):
        if num % i == 0:
            total += i
    return total == num