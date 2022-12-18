def log(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        print(func.headers)
        with open("log.txt", "a", encoding="UTF-8") as file_out:
            print(func(*args, **kwargs), file=file_out)
        return func(*args, **kwargs)
    return wrapper
