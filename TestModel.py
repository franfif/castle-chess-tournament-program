import names
from RandomDate import random_date
import random
import lorem


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


class TestTournament:
    def __init__(self):
        self.name = 'Event ' + names.get_full_name()
        self.venue = 'Venue ' + names.get_full_name()
        self.date = (random_date("01/01/2022", "06/30/2022", random.random()),
                     random_date("07/01/2022", "12/31/2022", random.random()))
        self.number_of_rounds = random.randint(0, 9)
        self.rounds = []
        self.players = []
        self.time_control = random.choice([0, 1, 2])
        self.description = lorem.sentence()

    def get_data(self):
        return (self.name,
                self.venue,
                self.date,
                self.number_of_rounds,
                self.rounds,
                self.players,
                self.time_control,
                self.description)
