from re import fullmatch


regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

def check_valid(email: str):
    if fullmatch(regex, email):
        return True
    return False