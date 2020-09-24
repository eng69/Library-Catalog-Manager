# ACIT 2515 - Assignment 4
# catalog_manager.py
# Group 19

"""
CatalogManager program that contains a catalog of library media items
"""

from catalog_stats import CatalogStats
from datetime import date, datetime
from multimedia import Multimedia
from books import Books
import math


class CatalogManager:
    """CatalogManager class"""
    def __init__(self, lib_name: str, ):
        """Initializes constructor"""
        if self._valid_string(lib_name, "library_name"):
            self._lib_name = lib_name.strip()
        self._catalog = list(Books.select()) + list(Multimedia.select())

    @staticmethod
    def _is_valid_isbn(isbn: int) -> bool:
        if type(isbn) is not int:
            raise TypeError("ISBN should be an integer")
        elif int(math.log10(isbn)) + 1 not in [10, 13]:
            raise ValueError("ISBN should be either 10 digit or 13 digit.")
        else:
            return True

    @staticmethod
    def _valid_string(string, str_name):
        """Validates string"""
        if type(string) is not str:
            raise TypeError(f"Invalid {str_name}. Must be a string.")
        elif string.strip() == "":
            raise ValueError(f"Invalid {str_name}. Must not be empty.")
        return True

    def add_item(self, item):
        """Adds media item to the catalog"""
        if type(item) not in [Books, Multimedia]:
            raise ValueError("Only books and multimedia can add to the catalog.")
        if item.isbn in [i.isbn for i in self._catalog]:
            raise ValueError("Item with the same isbn already exist")
        self._catalog.append(item)
        item.save_item()

    def get_item_by_isbn(self, isbn):
        """Returns item in the catalog with matching ISBN"""
        if self._is_valid_isbn(isbn):
            try:
                item = (Books.select().where(Books.isbn == isbn) or
                        Multimedia.select().where(Multimedia.isbn == isbn)).get()
                return item
            except:
                return None

    def get_items_by_type(self, type_):
        """Returns items by type"""
        if self._valid_string(type_, "type"):
            items = []
            if type_ == "books":
                return Books.select()
            elif type_ == "multimedia":
                return Multimedia.select()
            else:
                return items

    def get_all_items(self):
        """Returns a list of all items in the catalog"""
        return list(Books.select()) + list(Multimedia.select())

    def delete_item_by_isbn(self, ISBN):
        """ Deletes item in the catalog """
        if self._is_valid_isbn(ISBN):
            item = self.get_item_by_isbn(ISBN)
            if item:
                item.delete_instance()
                self._catalog.remove(item)

    def get_borrow_items(self):
        """Returns a list of borrowed items in the catalog"""
        items = []
        items = list(Books.select().where(Books.is_borrowed)) + list(Multimedia.select().where(Multimedia.is_borrowed))
        return items

    def get_overdue_items(self):
        """Returns a list of overdue items in the catalog"""
        items = []
        for item in self.get_borrow_items():
            if item.get_due_date() < date.today():
                items.append(item)
        return items

    def get_overdue_fees(self):
        """Returns total overdue fees for the catalog"""
        total_fees = 0
        for item in self.get_overdue_items():
            if item.get_due_date() < date.today():
                total_fees += item.get_fee()
        return total_fees

    def get_stats(self):
        """Returns catalog statistics"""
        num_books = len(self.get_items_by_type("books"))
        num_media = len(self.get_items_by_type("multimedia"))
        num_borrowed = len(self.get_borrow_items())
        num_available = len(self.get_all_items()) - num_borrowed
        num_overdue = len(self.get_overdue_items())
        total_fees = self.get_overdue_fees()

        stats = CatalogStats(num_books, num_media, num_borrowed, num_available, num_overdue, total_fees)
        return stats

    def to_dict(self):
        """ Generate a dictionary representation of the catalog manager """
        output_dict = [item.to_dict() for item in self.get_all_items()]
        return output_dict

    def add_item_from_json(self, item):
        """ Import an item to the catalog manager from a json formatted object """
        if item["type_"] == "multimedia":
            entity = Multimedia(isbn=item["isbn"], author=item["author"], publisher=item["publisher"], title=item["title"],
                                genre=item["genre"], pub_date=datetime.strptime(item["pub_date"].strip(), "%Y-%m-%d"),
                                is_borrowed=item["is_borrowed"], borrow_date=datetime.strptime(item["borrow_date"].strip(), "%Y-%m-%d"),
                                length=(datetime.strptime(item["length"].strip(), "%H:%M:%S").time()),
                                sub_type=item["sub_type"], type_=item["type_"])
            self.add_item(entity)
        elif item["type_"] == "books":
            entity = Books(isbn=item["isbn"], author=item["author"], publisher=item["publisher"], title=item["title"],
                           genre=item["genre"], pub_date=datetime.strptime(item["pub_date"].strip(), "%Y-%m-%d"),
                           is_borrowed=item["is_borrowed"], borrow_date=item["borrow_date"],
                           length=(item["length"]), sub_type=item["sub_type"], type_=item["type_"])
            self.add_item(entity)
