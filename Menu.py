from BaseView import BaseView


class Menu:
    def __init__(self):
        self.view = BaseView()
        # self.options = options

    def run_menu(self, options, obj):
        next_action = None
        while next_action is None:
            # menu = self.new_app_menu()
            option_names = list(map(lambda x: x.name, options))
            to_do = self.view.select_from_list(option_names)
            do_it = options[to_do].function
            obj.do_it()
