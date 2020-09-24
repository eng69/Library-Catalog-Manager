# ACIT 2515: Assignment 2 - Catalog Stats
# Author: Eric Ng
# Date: Feb. 25, 2020

"""CatalogStats program that contains catalog statistics"""

class CatalogStats:
    """CatalogStats class"""
    def __init__(self, num_books, num_media, num_borrowed, num_available, num_overdue, total_fees):
        """Initializes constructor"""
        if self._valid_int(num_books, "num_books"):
            self._num_books = num_books
        if self._valid_int(num_media, "num_media"):
            self._num_media = num_media
        if self._valid_int(num_borrowed, "num_borrowed"):
            self._num_borrowed = num_borrowed
        if self._valid_int(num_available, "num_available"):
            self._num_available = num_available
        if self._valid_int(num_overdue, "num_overdue"):
            self._num_overdue = num_overdue
        if type(total_fees) not in (int, float):
            raise TypeError(f"Invalid total_fees. Must be a float or an integer")
        elif total_fees < 0:
            raise ValueError(f"Invalid total_fees. Must not be negative")
        self._total_fees = total_fees

    def to_dict(self):
        """ Return a dictionary representation of the catalog stats """
        return {
            "num_books": self._num_books,
            "num_media": self._num_media,
            "num_borrowed": self._num_borrowed,
            "num_available": self._num_available,
            "num_overdue": self._num_overdue,
            "total_fees": self._total_fees
        }

    @staticmethod
    def _valid_int(num, attribute):
        """Validates attribute"""
        if type(num) is not int:
            raise TypeError(f"Invalid {attribute}. Must be an integer.")
        elif num < 0:
            raise ValueError(f"Invalid {attribute}. Must not be negative.")
        return True

    def get_num_books(self):
        """Returns the number of books in the catalog"""
        return self._num_books

    def get_num_media(self):
        """Returns the number of multimedia in the catalog"""
        return self._num_media

    def get_num_borrowed(self):
        """Returns the number of borrowed items in the catalog"""
        return self._num_borrowed

    def get_num_available(self):
        """Returns the number of available items in the catalog"""
        return self._num_available

    def get_num_overdue(self):
        """Returns the number of overdue items in the catalog"""
        return self._num_overdue

    def get_total_fees(self):
        """Returns the total fees for the catalog"""
        return self._total_fees
