import random
import string


def random_str(N):
    """
    Для создания случайных строк определенной длины
    """
    return ''.join(random.choice(string.ascii_letters) for _ in range(N))
