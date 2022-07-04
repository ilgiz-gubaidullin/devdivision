import dataclasses
from final_project.helpers.utility_functions import random_str
from dataclasses import dataclass
from faker import Faker


fake = Faker()


class DataManager:

    @staticmethod
    def user(name=None, surname=None, middle_name=None, username=None, password=None, email=None):
        @dataclass
        class User:
            name: str
            surname: str
            middle_name: str
            username: str
            password: str
            email: str

        user = User(
            name=name if name is not None else fake.first_name(),
            surname=surname if surname is not None else fake.last_name(),
            middle_name=middle_name if middle_name is not None else fake.first_name(),
            username=username if username is not None else random_str(15),
            password=password if password is not None else fake.password(),
            email=email if email is not None else fake.email()
        )

        return dataclasses.asdict(user)