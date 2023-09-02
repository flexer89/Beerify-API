def has_one_decimal_place(rating: float) -> bool:
    rating_str = str(rating)
    parts = rating_str.split('.')
    
    if len(parts) == 2 and len(parts[1]) == 1:
        return True
    else:
        return False
