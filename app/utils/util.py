def has_one_decimal_place(rating: float) -> bool:
    rating_str = str(rating)
    parts = rating_str.split('.')
    
    if len(parts[1]) == 1 or len(parts[1] == 0):
        return True
    else:
        return False


print(has_one_decimal_place(5.0))