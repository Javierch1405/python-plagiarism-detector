def sort_list(a: list[int]) -> list[int]:
    return sorted(a)


if __name__ == "__main__":
    import sys
    arr = list(map(int, sys.stdin.read().split())) or [3, 1, 2]
    print(sort_list(arr))
