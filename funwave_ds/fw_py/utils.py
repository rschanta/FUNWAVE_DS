


# Helper function to convert to valid FORTRAN
def convert_to_number(value):
    try:
        # Try conversion to float (will work for ints/floats)
        float_value = float(value)
        
        # Case to return float: if a decimal point is provided
        if '.' in str(value).strip():
            return float_value
        # Case to return int: if no decimal point is provided
        else: 
            return int(float_value)
        
    # Case to return string: if conversion to float fails
    except ValueError:
        return value
        