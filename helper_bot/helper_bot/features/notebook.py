from typing import Any, List
from datetime import date
import re

from helper_bot.helper_bot.features.bot_feature import BotFeature
from helper_bot.helper_bot.features.records_container import RecordsContainer

NAME_REGEX = re.compile(r"[a-zA-Zа-яА-Я0-9,.'\w]{2,30}")


class NoteField:

    def __init__(self, value) -> None:
        self._value = None
        self.value = value

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value) -> None:
        self._value = value


class Title(NoteField):

    @NoteField.value.setter
    def value(self, title: str):
        if not re.match(NAME_REGEX, title):
            raise ValueError("Title must be between 2 and 30 characters.")
        self._value = title

    def __hash__(self):
        return self.value.__hash__()

    def __eq__(self, obj):
        return self.value == obj


class NoteRecord:

    def __init__(self, title: str, text: str, tags: List[str]) -> None:
        self.name = Title(title)
        self.text = text
        self.created = date.today()
        self.tags = tags

    def __str__(self) -> str:
        return f'{self.name.value}\n{self.text}\n{", ".join([p for p in self.tags])}\n{self.created}'

    def change_title(self, new_title: str) -> None:
        """
        Changes the title of the note.

        :param new_title: a new title
        """

        self.name = Title(new_title)

    def change_tags(self, *args: str) -> None:
        """
        Changes the tags of the note.

        :param args: new tags
        """

        self.tags.clear()
        self.tags = list(args)

    def change_text(self, new_text: str) -> None:
        """
        Changes the text of the note.

        :param new_text: a new text
        """

        self.text = new_text


class Notebook(BotFeature):
    """
    An app feature that helps users to manage their notes.
    """

    def __init__(self, save_file: str):
        self.save_file = save_file
        self.data = RecordsContainer(save_file)

        super().__init__({
            "make": (self.make_note, "notes make"),
            "change": (self.change_note, "notes change title"),
            "remove": (self.data.remove_record, "notes remove title"),
            "show": (self.data.show_all, "notes show "),
            "search": (self.data.search_record, "notes search tag/title/text")
            })

    @staticmethod
    def name():
        return "notes"

    def make_note(self) -> str:
        """
        Creates a new note. Raises exception if note with a given title already exists.

        :return: success message
        """

        title = input('Enter the title: ').strip()

        if self.data.record_exists(title):
            raise f"Note {title} already exists! Try another name."

        text = input('Enter the text: ')
        tags = input('Enter the tags: ').strip().split()
        note = NoteRecord(title, text, tags)
        self.data.add_record(note)
        return f"Note {title} was created successfully!"

    def change_note(self, *args: str) -> str:
        """
        Changes existing notes. Raises exception if a note that the user wants to change does not exist.

        :param args: note title
        :return: success message
        """

        title = " ".join(args)
        if self.data.record_exists(title):
            note_to_change = self.data[title]
            while True:
                to_change = input("What do you want to change? Type title, tags or text: ")
                if to_change.lower() not in ["title", "tags", "text"]:
                    print("Unknown command")
                    continue
                elif to_change.lower() == "title":
                    new_title = input("Enter a new title: ")
                    note_to_change.change_title(new_title)
                    self.data.add_record(note_to_change)
                    self.data.remove_record(title)
                elif to_change.lower() == "tags":
                    new_tags = input("Enter new tags: ")
                    note_to_change.change_tags(new_tags)
                elif to_change.lower() == "text":
                    new_text = input("Enter new text here: ")
                    note_to_change.change_text(new_text)

                to_continue = input("Do you want to change something else in this note? Enter y or n: ")
                if to_continue.lower() not in ["y", "n"]:
                    print("Enter y or n.")
                    continue
                elif to_continue.lower() == "y":
                    continue
                else:
                    return "The note was changed successfully!"
        else:
            raise KeyError("Note with this title doesn't exist.")
