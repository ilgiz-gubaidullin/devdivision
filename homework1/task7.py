import datetime


def timedif(func):
    def wrapper():
        start = datetime.datetime.now()
        result = func()
        print(datetime.datetime.now() - start)
        return result
    return wrapper


@timedif
def func():
    import random
    import time
    time.sleep(random.randint(0, 10))

func()  # prints this execution time
func()  # prints this execution time
func()  # prints this execution time