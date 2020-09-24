# ACIT 2515 - Assignment 4
# books.py
# Group 19

"""
The books class
"""

from abstract_catalog import AbstractCatalog
import datetime

class Books(AbstractCatalog):

    def get_details(self) -> str:
        """ Return a description of the book """
        output = f"{self.title} by {self.author} (ISBN: {self.isbn}) " \
                 f"is a {self.length} page {self.sub_type} book. \n" \
                 f"Published on {datetime.datetime.strftime(self.pub_date, '%Y-%m-%d')} by {self.publisher}\n"
        if self.get_borrow_date():
            output += f"[Borrowed on {self.get_borrow_date()}] " \
                      f"[Due on {datetime.datetime.strftime(self.get_due_date(), '%Y-%m-%d')}] \n"
            if datetime.datetime.today().date() > self.get_due_date().date():
                output += f"Overdue by {(datetime.datetime.today() - self.get_due_date()).days} days. \n" \
                          f"${self.get_fee():.02f} fee receivables.\n"
        return output

    def save_item(self):
        """ Set the type of item before saving """
        self.save(force_insert=True)

    def to_dict(self) -> dict:
        """ Return a dictionary representation of a book object """
        return {
            "isbn": self.isbn,
            "author": self.author,
            "publisher": self.publisher,
            "title": self.title,
            "genre": self.genre,
            "pub_date": datetime.datetime.strftime(self.pub_date, "%Y-%m-%d"),
            "is_borrowed": bool(self.is_borrowed),
            "borrow_date": datetime.datetime.strftime(self.borrow_date, "%Y-%m-%d") if self.is_borrowed else None,
            "length": self.length,
            "sub_type": self.sub_type,
            "type_": self.type_
        }
