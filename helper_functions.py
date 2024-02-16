def longerThan(value, length, message):
    while len(value) > length:
        print(f"{message} is longer than {length} characters")
        value = input("Enter a new {message}: ")
    return value