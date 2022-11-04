from tinydb import TinyDB


class TableDB:
    def __init__(self, name):
        self.db = TinyDB('db.json')
        self.table = self.db.table(name)

    def insert_multiple(self, items):
        self.table.truncate()
        self.table.insert_multiple(items)

    def get_all_items(self):
        return self.table.all()
