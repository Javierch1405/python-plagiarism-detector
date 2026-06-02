def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


if __name__ == "__main__":
    import sys
    try:
        n = int(sys.argv[1])
    except Exception:
        n = 17
    print(is_prime(n))
