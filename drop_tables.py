# ACIT 2515 - Assignment 4
# drop_tables.py
# Group 19

"""
This file drop the table structure of the database
"""

from database import db
from books import Books
from multimedia import Multimedia

if __name__ == "__main__":
    db.drop_tables([Books, Multimedia])