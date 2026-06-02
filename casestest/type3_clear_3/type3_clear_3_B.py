def sort_list(a: list[int]) -> list[int]:
    # simple insertion sort implementation
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


if __name__ == "__main__":
    import sys
    arr = list(map(int, sys.stdin.read().split())) or [3, 1, 2]
    print(sort_list(arr))
