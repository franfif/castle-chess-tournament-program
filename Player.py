class Player:
    def __init__(self, first_name, last_name, date_of_birth,
                 gender, ranking, player_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.ranking = ranking
        if player_id is None:
            self.id = self.__hash__()
        else:
            self.id = player_id

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name
