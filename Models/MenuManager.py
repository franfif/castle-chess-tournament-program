from Views.BaseView import BaseView


class MenuManager:

    @staticmethod
    def menu(get_options_method, save_method=None, titles=None, content=None):
        next_action = None
        while next_action is None:
            if titles is not None:
                # Evaluate callbacks in titles if needed
                checked_titles = titles
                if isinstance(titles, tuple):
                    checked_titles = tuple(map(lambda x: (x() if callable(x) else x), titles))
                BaseView.display_title(checked_titles)
            if content is not None:
                content[0](content[1])
            menu = get_options_method()
            menu_names = list(map(lambda x: x.name, menu))
            to_do = BaseView.select_from_list(menu_names)
            next_action = menu[to_do].function()
            if save_method is not None:
                save_method()
        return

    @staticmethod
    def exit():
        return True
