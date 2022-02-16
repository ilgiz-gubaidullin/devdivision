# Первый способ через класс
class Context:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"Привет, {self.name}!")
        return self

    def letters(self):
        s = str(self.name)
        for i in s.upper():
            print(i * 3)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Пока, {self.name}!")

with Context('Яна') as c:
    c.letters()

# Второй способ через функцию

def context(name):
    print(f"Привет, {name}!")
    try:
        s = str(name)
        for i in s.upper():
            print(i * 3)
    finally:
        print(f"Пока, {name}!")

context("Аня")