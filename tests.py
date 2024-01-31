import unittest
from datetime import time

from library import Library, Book, AudioBook, Movie, Patron


class TestingPatrons(unittest.TestCase):

    def test_create_patron(self):
        pat1 = Patron("Katie")
        self.assertEqual(pat1.borrowed_items, [])

    def test_add_patron(self):
        pat1 = Patron("Katie")
        lib = Library()
        self.assertEqual(lib.patrons, [])
        lib.add_patrons([pat1])
        self.assertEqual(lib.patrons, [pat1])

    def test_remove_patron(self):
        pat1 = Patron("Katie")
        lib = Library()
        lib.add_patrons([pat1])
        self.assertEqual(lib.patrons, [pat1])
        lib.remove_patrons([pat1])
        self.assertEqual(lib.patrons, [])

    def test_remove_fake_patron(self):
        pat1 = Patron("Katie")
        pat2 = Patron("Sarah")
        lib = Library()
        lib.add_patrons([pat1])
        self.assertEqual(lib.patrons, [pat1])
        lib.remove_patrons([pat2])
        self.assertEqual(lib.patrons, [pat1])

    def test_borrow_item(self):
        pat1 = Patron("Katie")
        lib = Library()
        lib.add_patrons([pat1])
        book1 = Book("Harry Potter", 300)
        lib.add_items([book1])
        self.assertEqual(pat1.borrowed_items, [])
        self.assertEqual(lib.items[1].available, True)
        pat1.borrow_item(1, lib)
        self.assertEqual(pat1.borrowed_items, [book1])
        self.assertEqual(lib.items[1].available, False)

    def test_borrow_fake_item(self):
        pat1 = Patron("Katie")
        lib = Library()
        lib.add_patrons([pat1])
        self.assertEqual(pat1.borrowed_items, [])
        pat1.borrow_item(1, lib)
        self.assertEqual(pat1.borrowed_items, [])

    def test_borrow_unavailable_item(self):
        pat1 = Patron("Katie")
        pat2 = Patron("Sarah")
        lib = Library()
        lib.add_patrons([pat1])
        book1 = Book("Harry Potter", 300)
        lib.add_items([book1])
        self.assertEqual(pat2.borrowed_items, [])
        pat1.borrow_item(1, lib)
        pat2.borrow_item(1, lib)
        self.assertEqual(pat2.borrowed_items, [])

    def test_return_item(self):
        pat1 = Patron("Katie")
        lib = Library()
        lib.add_patrons([pat1])
        book1 = Book("Harry Potter", 300)
        lib.add_items([book1])
        pat1.borrow_item(1, lib)
        pat1.return_item(1, lib)
        self.assertEqual(pat1.borrowed_items, [])
        self.assertEqual(lib.items[1].available, True)

    def test_return_fake_item(self):
        pat1 = Patron("Katie")
        lib = Library()
        lib.add_patrons([pat1])
        book1 = Book("Harry Potter", 300)
        lib.add_items([book1])
        pat1.borrow_item(1, lib)
        pat1.return_item(2, lib)
        self.assertEqual(pat1.borrowed_items, [book1])
        self.assertEqual(lib.items[1].available, False)


class TestingLibrary(unittest.TestCase):

    def test_create_library(self):
        lib = Library()
        self.assertEqual(lib.items, {})
        self.assertEqual(lib.patrons, [])
        self.assertEqual(lib._counter, 1)

    def test_counter(self):
        lib = Library(counter=5)
        self.assertEqual(lib._counter, 5)
        book1 = Book("Harry Potter", 300)
        lib.add_items([book1])
        self.assertEqual(lib._counter, 6)

    def test_str(self):
        book1 = Book("Harry Potter", 300)
        ab1 = AudioBook("Percy Jackson", time(10, 3, 25), time(0, 0, 0))
        movie1 = Movie("Twilight", time(2, 20, 3), time(0, 0, 0))
        pat1 = Patron("Katie")
        pat2 = Patron("Sarah")
        pat3 = Patron("Mary")
        lib = Library()
        lib.add_items([book1, ab1, movie1])
        lib.add_patrons([pat1, pat2, pat3])
        pat3.borrow_item(2, lib)
        pat3.borrow_item(1, lib)
        pat1.borrow_item(3, lib)
        self.assertEqual(str(lib),
                         ("PATRONS\n"
                          "Katie has borrowed...\n"
                          "	Twilight\n"
                          "Sarah has borrowed...\n"
                          "Mary has borrowed...\n"
                          "	Percy Jackson\n"
                          "	Harry Potter\n"
                          "ITEMS\n"
                          "	Harry Potter\n"
                          "	Percy Jackson\n"
                          "	Twilight\n"))


class TestingLibraryItems(unittest.TestCase):

    def test_books(self):
        book1 = Book("Harry Potter", 300)
        self.assertEqual(book1.id, -1)
        self.assertEqual(book1.available, True)
        self.assertEqual(book1.current_page, 0)
        self.assertEqual(book1.title, "Harry Potter")
        self.assertEqual(book1.pages, 300)
        self.assertEqual(str(book1), "Harry Potter")

    def test_audio_books(self):
        ab1 = AudioBook("Percy Jackson", time(10, 3, 25), time(0, 0, 0))
        self.assertEqual(ab1.id, -1)
        self.assertEqual(ab1.available, True)
        self.assertEqual(ab1.current_time, time(0, 0, 0))
        self.assertEqual(ab1.title, "Percy Jackson")
        self.assertEqual(ab1.length, time(10, 3, 25))
        self.assertEqual(str(ab1), "Percy Jackson")

    def test_movies(self):
        movie1 = Movie("Twilight", time(2, 20, 3), time(0, 0, 0))
        self.assertEqual(movie1.id, -1)
        self.assertEqual(movie1.available, True)
        self.assertEqual(movie1.current_time, time(0, 0, 0))
        self.assertEqual(movie1.title, "Twilight")
        self.assertEqual(movie1.length, time(2, 20, 3))
        self.assertEqual(str(movie1), "Twilight")


if __name__ == '__main__':
    unittest.main()
