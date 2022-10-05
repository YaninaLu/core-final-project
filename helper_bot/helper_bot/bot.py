from typing import List, Any, Callable

from helper_bot.helper_bot.features.addressbook import AddressBook
from helper_bot.helper_bot.features.files import Files
from helper_bot.helper_bot.features.notebook import Notebook

ADDRESS_BOOK_FILE = "address_book.bin"
NOTEBOOK_FILE = "notebook.bin"


class AssistantBot:
    """
    Assists a user with managing the features of the application.
    """

    def __init__(self):
        self.features = [
            Files(),
            Notebook(NOTEBOOK_FILE),
            AddressBook(ADDRESS_BOOK_FILE)
        ]

    @staticmethod
    def input_error(func: Callable) -> Callable[[tuple[Any, ...]], str | Any]:
        """
        A decorator that catches the domain-level exceptions and returns human-readable error message.
        """

        def exception_handler(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except TypeError as err:
                return f"Invalid input, some info is missing: {err}"
            except KeyError as err:
                return f"Sorry: {err}"
            except ValueError as err:
                return f"ValueError: {err}"
            else:
                return result

        return exception_handler

    @input_error
    def handle(self, handler_name: str, args: List[str]) -> str:
        """
        Calls the commands of the features and returns results.

        :param handler_name: command given by the user
        :param args: arguments to call the command with
        :return: result of execution of the command
        """

        command_handler = self._get_handler(handler_name)

        if command_handler:
            command_arguments = args[1:] if len(args) > 1 else []
            return command_handler.handle_command(args[0], *command_arguments)
        else:
            raise ValueError(f"Unexpected command: {command_handler}")

    def _get_handler(self, handler_name: str) -> Any:
        handler = next(filter(lambda x: x.name() == handler_name, self.features), None)
        return handler

    def autocomplete(self) -> List:
        """
        Creates a list of autocomplete commands.

        :return: list of possible commands
        """
        result = ["help"]
        for feature in self.features:
            for command_name in feature.command_handlers.keys():
                result.append(f"{feature.name()} {command_name}")
        return result

    def backup_data(self):
        """
        Saves user data to files.
        """
        for handler in self.features:
            if hasattr(handler, "data"):
                handler.data.backup_data(handler)

    def help(self):
        result = "To work with a bot type in:\n"
        for feature in self.features:
            for key, value in feature.command_handlers.items():
                result += "- " + value[1] + "\n"
        return result
