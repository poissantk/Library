import logging
import time
import logging
from library import AudioBook, Movie, Book
import datetime as dt


def timer(func):
    def inner(*args, **kwargs):
        begin = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        print(f"Function took {end - begin} seconds to run")
        return value
    return inner


class ItemFactory:

    @staticmethod
    def build_item(item_type: str):
        if item_type == "book":
            return Book("Default Name", 0)
        if item_type == "audiobook":
            return AudioBook("Default Name", dt.time(0, 0, 0))
        if item_type == "movie":
            return Movie("Default Name", dt.time(0, 0, 0))
        else:
            logging.warning("Please provide 'book', 'audiobook', or 'movie'")
            return -1
