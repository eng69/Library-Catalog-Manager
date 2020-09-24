# ACIT 2515 - Assignment 4
# create_tables.py
# Group 19

"""
Creates the table structure of the database
"""

from database import db
from books import Books
from multimedia import Multimedia

if __name__ == "__main__":
    db.create_tables([Books, Multimedia])
