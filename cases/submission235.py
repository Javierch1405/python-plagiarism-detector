def calculate_bmi(weight_kg, height_m):
    if height_m <= 0:
        return 0
    return weight_kg / (height_m ** 2)