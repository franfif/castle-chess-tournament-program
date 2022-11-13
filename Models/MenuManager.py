from Views.BaseView import BaseView


class MenuManager:

    @staticmethod
    def menu(get_options_method, save_method=None, titles=None, content=None):
        """
        Put together a menu of options, with titles, content, and a saving method
        :param get_options_method: a callback to update the menu options
        :param save_method: optional, a callback to save the changes to the database
        :param titles: optional, a single string or a tuple of strings to display above the menu
        :param content: optional, a pair containing a callback and a parameter for the callback
        :return: nothing
        """
        next_action = None
        while next_action is None:
            if titles is not None:
                # Evaluate callbacks in titles if needed
                checked_titles = titles
                if isinstance(titles, tuple):
                    checked_titles = tuple(map(lambda x: (x() if callable(x) else x), titles))
                BaseView.display_titles(checked_titles)
            # Display content
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
        """Default exit method, return True."""
        return True
