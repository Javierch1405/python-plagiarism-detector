def count_evens(numbers):
    evens = [n for n in numbers if n % 2 == 0]
    return len(evens)