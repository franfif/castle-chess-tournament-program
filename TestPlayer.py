import names
from RandomDate import random_date
import random


class TestPlayer:
    def __init__(self):
        self.first_name = names.get_first_name()
        self.last_name = names.get_last_name()
        self.date_of_birth = random_date("1/1/1930",
                                         "1/1/2009",
                                         random.random())
        self.sex = random.choice(['M', 'F', 'X'])
        self.ranking = random.randint(0, 2999)

    def get_data(self):
        return (self.first_name,
                self.last_name,
                self.date_of_birth,
                self.sex,
                self.ranking)
