# ACIT 2515 - Assignment 2
# abstract_catalog.py
# Group 19

"""
This python file contains an AbstractCatalog class
"""

import datetime
import math
from peewee import Model, CharField, IntegerField, DateField, BooleanField, AutoField
from database import db

class AbstractCatalog(Model):

    _LATE_CHARGES_PER_DAY = 0.3

    # uid = AutoField()
    isbn = IntegerField(primary_key=True)
    author = CharField()
    publisher = CharField()
    title = CharField()
    genre = CharField()
    pub_date = DateField()
    is_borrowed = BooleanField(null=True)
    borrow_date = DateField(null=True)
    length = CharField()
    sub_type = CharField()
    type_ = CharField()

    class Meta:
        database = db

    def get_fee(self):
        """ Getter overdue fee """
        if self.get_due_date():
            fee = self._LATE_CHARGES_PER_DAY * (datetime.date.today() - self.get_due_date()).days
            if fee <= 0:
                return 0
            else:
                return fee
        else:
            return 0

    def borrow(self, date: str):
        """ Borrow an item """
        if self.is_borrowed:
            raise RuntimeError("The item is already borrowed")
        self.borrow_date = datetime.datetime.strptime(date, "%Y-%m-%d")
        self.is_borrowed = True
        self.save()

    def return_item(self):
        """ Return an item """
        if not self.is_borrowed:
            raise RuntimeError("This item is not borrowed.")
        self.is_borrowed = False
        self.borrow_date = None
        self.save()

    def get_borrow_date(self) -> str:
        """ Get the borrow in string format """
        if self.borrow_date:
            return datetime.datetime.strftime(self.borrow_date, "%Y-%m-%d")
        else:
            return None

    def get_due_date(self) -> datetime.datetime:
        """ Get the due date in datetime format """
        if self.borrow_date:
            return self.borrow_date + datetime.timedelta(days=4 * 7)
        else:
            return None

    def save_item(self):
        """ Abstract method call before save, please implement on sub class """
        raise NotImplementedError("Function not implemented, please implement in sub class")