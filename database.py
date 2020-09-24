# ACIT 2515 - Assignment 4
# database.py
# Group 19

"""
This python file provides connection to the database
"""

from peewee import SqliteDatabase

db = SqliteDatabase("catalog.sqlite")
db.connect()
