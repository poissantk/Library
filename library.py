import datetime
import datetime as dt
import logging
from time import sleep

from utils import timer


class Library:

    def __init__(self, items: dict = None, patrons: list = None, counter: int = 1):
        if patrons is None:
            patrons = []
        if items is None:
            items = {}
        self.items = items
        self.patrons = patrons
        self._counter = counter

    def __str__(self):
        value = "PATRONS\n"
        for patron in self.patrons:
            value += str(patron)
        value += "ITEMS\n"
        for item_key in self.items.keys():
            value += ("\t" + str(self.items[item_key]) + "\n")
        return value

    def add_items(self, new_items):
        for item in new_items:
            item.id = self._counter
            self._counter += 1
            self.items[item.id] = item

    def remove_items(self, old_items):
        for item in old_items:
            if item in self.items:
                del self.items[item.id]
            else:
                logging.warning("Library item not in library!")

    def add_patrons(self, new_patrons):
        for patron in new_patrons:
            self.patrons.append(patron)

    def remove_patrons(self, old_patrons):
        for patron in old_patrons:
            if patron in self.patrons:
                self.patrons.remove(patron)
            else:
                logging.warning("Library patron not in library!")

    @property
    def counter(self):
        return self._counter

    @counter.setter
    def counter(self, value):
        if value < self._counter:
            raise Exception("The counter can't go backwards!")
        else:
            self._counter = value


class LibraryItem:

    def __init__(self, title: str):
        self.id = -1
        self.title = title
        self.available = True

    def __str__(self):
        return self.title


class Book(LibraryItem):
    def __init__(self, title: str, pages: int, current_page: int = 0):
        super().__init__(title)
        self.pages = pages
        self.current_page = current_page


class Movie(LibraryItem):
    def __init__(self, title: str, length: datetime.time, current_time: datetime.time = dt.time(0, 0, 0)):
        super().__init__(title)
        self.length = length
        self.current_time = current_time


class AudioBook(LibraryItem):
    def __init__(self, title: str, length: datetime.time, current_time: datetime.time = dt.time(0, 0, 0)):
        super().__init__(title)
        self.length = length
        self.current_time = current_time


class Patron:
    def __init__(self, name: str):
        self.name = name
        self.borrowed_items = []

    def __str__(self):
        value = f"{self.name} has borrowed...\n"
        for item in self.borrowed_items:
            value += ("\t" + str(item) + "\n")
        return value

    def borrow_item(self, borrow_id, library):
        if borrow_id in library.items.keys():
            if library.items[borrow_id].available:
                self.borrowed_items.append(library.items[borrow_id])
                library.items[borrow_id].available = False
            else:
                logging.warning("Item you want to borrow is unavailable")
        else:
            logging.warning("Item you want to borrow is not at this library")

    def return_item(self, return_id, library):
        if return_id in library.items.keys():
            self.borrowed_items.remove(library.items[return_id])
            library.items[return_id].available = True
        else:
            logging.warning("Item you want to return is not from this library")


@timer
def scenario():
    book1 = Book("Harry Potter", 300)
    ab1 = AudioBook("Percy Jackson", dt.time(10, 3, 25), dt.time(0, 0, 0))
    movie1 = Movie("Twilight", dt.time(2, 20, 3), dt.time(0, 0, 0))
    pat1 = Patron("Katie")
    pat2 = Patron("Sarah")
    pat3 = Patron("Mary")
    lib = Library()
    lib.add_items([book1, ab1, movie1])
    lib.add_patrons([pat1, pat2, pat3])
    pat3.borrow_item(2, lib)
    pat3.borrow_item(1, lib)
    pat1.borrow_item(3, lib)
    pat1.borrow_item(4, lib)
    pat2.borrow_item(1, lib)
    print(lib)
    print("*******************")
    pat3.return_item(2, lib)
    pat3.return_item(1, lib)
    pat1.return_item(3, lib)
    pat1.return_item(4, lib)
    print(lib)
    sleep(1)


if __name__ == "__main__":
    scenario()
