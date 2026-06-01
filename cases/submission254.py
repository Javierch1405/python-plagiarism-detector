def compound_interest(principal, rate, time, n):
    amount = principal * ((1 + rate / n) ** (n * time))
    return amount - principal