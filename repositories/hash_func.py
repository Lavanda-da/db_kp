def hash(string):
    result = 0
    for i in string:
        result = result * 199 + ord(i) / 11
    return str(result)