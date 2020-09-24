# ACIT 2515: Assignment 2 - Testing Catalog Manager
# Author: Eric Ng
# Date: Feb. 25, 2020
"""TestCatalogManager program that tests CatalogManager class"""

from unittest import TestCase, mock
from catalog_manager import CatalogManager
from books import Books
from multimedia import Multimedia
from catalog_stats import CatalogStats
import datetime
import json
from peewee import SqliteDatabase

test_db = SqliteDatabase('testdb.sqlite')

class TestCatalogManager(TestCase):
    """TestCatalogManager class"""

    def setUp(self):
        """Creates catalog manager object for testing"""
        test_db.bind([Books, Multimedia])
        test_db.create_tables([Books, Multimedia])
        self.catalog_manager1 = CatalogManager("Catalog1")
        self.valid_multimedia = Multimedia(isbn=1234567891023, author="Eric N", publisher="BE Publishing", title="1000 night at school",
                                           genre="romantic", pub_date=datetime.date(2020, 1, 30), length="01:32:24", sub_type="CD", type_="multimedia")
        self.valid_borrowed_multimedia = Multimedia(isbn=1234567891024, author="Eric K", publisher="KE Publishing", title="BCIT First look",
                                                    genre="informative", pub_date=datetime.date(2018, 2, 13), length="01:32:24", sub_type="Bluray", type_="multimedia")
        self.valid_borrowed_multimedia.borrow(datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m-%d"))
        self.valid_overdue_multimedia = Multimedia(isbn=1234567891025, author="Eric W", publisher="CA Publishing", title="Fairies",
                                                   genre="romantic", pub_date=datetime.date(1998, 1, 30), length="01:32:24", sub_type="VHS", type_="multimedia")
        self.valid_overdue_multimedia.borrow("1999-02-03")
        self.valid_Books = Books(isbn=1234567891026, author="Eric N", publisher="BE Publishing", title="1000 night at school",
                                 genre="romantic", pub_date=datetime.date(2020, 1, 30), length=324, sub_type="hardcover", type_="books")
        self.valid_borrowed_Books = Books(isbn=1234567891027, author="Eric K", publisher="KE Publishing", title="BCIT First look",
                                          genre="informative", pub_date=datetime.date(2018, 2, 13), length=134, sub_type="softcover", type_="books")
        self.valid_borrowed_Books.borrow(datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m-%d"))
        self.valid_overdue_Books = Books(isbn=1234567891028, author="Eric W", publisher="CA Publishing", title="Fairies",
                                         genre="romantic", pub_date=datetime.date(1998, 1, 30), length=688, sub_type="softcover", type_="books")
        self.valid_overdue_Books.borrow("1999-02-03")

    def tearDown(self) -> None:
        test_db.drop_tables([Books, Multimedia])
        test_db.close()

    def test_constructor(self):
        """Valid constructor 010A"""
        self.assertIsInstance(self.catalog_manager1, CatalogManager)

    def test_constructor_invalid(self):
        """Invalid constructor 100B"""
        with self.assertRaises(TypeError):
            CatalogManager(123)

        with self.assertRaises(ValueError):
            CatalogManager("  ")

    def test_add_item(self):
        """Valid item addition to catalog manager 020A """
        self.catalog_manager1.add_item(self.valid_Books)
        self.assertIn(self.valid_Books, self.catalog_manager1.get_all_items())
        self.catalog_manager1.add_item(self.valid_multimedia)
        self.assertIn(self.valid_multimedia, self.catalog_manager1.get_all_items())

    def test_add_item_invalid(self):
        """Invalid item addition to catalog manager 020B """
        with self.assertRaises(ValueError):
            self.catalog_manager1.add_item(123)

    def test_add_item_invalid_duplicated(self):
        """ Invalid item addition to catalog manager (same isbn) 020C """
        self.catalog_manager1.add_item(self.valid_Books)
        with self.assertRaises(ValueError):
            self.catalog_manager1.add_item(self.valid_Books)

    def test_get_item_by_isbn(self):
        """ Get an item with a valid isbn 030A """
        self.catalog_manager1.add_item(self.valid_Books)
        self.assertEqual(self.catalog_manager1.get_item_by_isbn(1234567891026), self.valid_Books)

    def test_get_item_by_isbn_invalid(self):
        """ Get item with an invalid isbn 030B """
        self.catalog_manager1.add_item(self.valid_Books)
        with self.assertRaises(TypeError):
            self.catalog_manager1.get_item_by_isbn("1234567891023")
        with self.assertRaises(ValueError):
            self.catalog_manager1.get_item_by_isbn(123456789)

    def test_get_item_by_isbn_nonexist(self):
        """ Get item with an nonexist isbn 030C """
        self.assertIsNone(self.catalog_manager1.get_item_by_isbn(1234567891099))

    def test_get_items_by_type(self):
        """ Get all items with type 040A """
        self.catalog_manager1.add_item(self.valid_Books)
        self.catalog_manager1.add_item(self.valid_borrowed_Books)
        self.catalog_manager1.add_item(self.valid_overdue_Books)
        self.catalog_manager1.add_item(self.valid_multimedia)
        self.catalog_manager1.add_item(self.valid_borrowed_multimedia)
        self.catalog_manager1.add_item(self.valid_overdue_multimedia)
        for item in self.catalog_manager1.get_items_by_type("book"):
            self.assertIsInstance(item, Books)
        for item in self.catalog_manager1.get_items_by_type("multimedia"):
            self.assertIsInstance(item, Multimedia)

    def test_get_items_by_type_invalid(self):
        """ Get all item with invalid type 040B """
        with self.assertRaises(ValueError):
            self.catalog_manager1.get_items_by_type(" ")
        with self.assertRaises(TypeError):
            self.catalog_manager1.get_items_by_type(321)

    def test_get_all_items(self):
        """ Get all items in the catalog manager 050A """
        self.catalog_manager1.add_item(self.valid_Books)
        self.catalog_manager1.add_item(self.valid_borrowed_Books)
        self.catalog_manager1.add_item(self.valid_overdue_Books)
        self.catalog_manager1.add_item(self.valid_multimedia)
        self.catalog_manager1.add_item(self.valid_borrowed_multimedia)
        self.catalog_manager1.add_item(self.valid_overdue_multimedia)
        all_items = self.catalog_manager1.get_all_items()
        self.assertEqual(len(all_items), 6)

    def test_delete_item_by_isbn(self):
        """Valid item removal from catalog manager 060A """
        self.catalog_manager1.add_item(self.valid_Books)
        self.assertIn(self.valid_Books, self.catalog_manager1.get_all_items())
        self.catalog_manager1.delete_item_by_isbn(1234567891026)
        self.assertNotIn(self.valid_Books, self.catalog_manager1.get_all_items())

    def test_delete_item_by_isbn_invalid(self):
        """Invalid item removal from catalog manager 060B """
        self.catalog_manager1.add_item(self.valid_Books)
        with self.assertRaises(TypeError):
            self.catalog_manager1.delete_item_by_isbn("1234567891026")
        with self.assertRaises(ValueError):
            self.catalog_manager1.delete_item_by_isbn(123456789102)

    def test_delete_item_by_isbn_invalid_not_exist(self):
        """Invalid item removal from catalog manager 060C """
        self.assertIsNone(self.catalog_manager1.delete_item_by_isbn(1234567891046))

    def test_get_borrowed_items(self):
        """ Get All Borrowed items 070A """
        self.catalog_manager1.add_item(self.valid_Books)
        self.catalog_manager1.add_item(self.valid_borrowed_Books)
        self.catalog_manager1.add_item(self.valid_overdue_Books)
        self.catalog_manager1.add_item(self.valid_multimedia)
        self.catalog_manager1.add_item(self.valid_borrowed_multimedia)
        self.catalog_manager1.add_item(self.valid_overdue_multimedia)
        for item in [self.valid_borrowed_Books,
                     self.valid_overdue_Books,
                     self.valid_borrowed_multimedia,
                     self.valid_overdue_multimedia]:
            self.assertIn(item, self.catalog_manager1.get_borrow_items())

    def test_get_overdue_items(self):
        """ Get all overdue items 080A """
        self.catalog_manager1.add_item(self.valid_Books)
        self.catalog_manager1.add_item(self.valid_borrowed_Books)
        self.catalog_manager1.add_item(self.valid_overdue_Books)
        self.catalog_manager1.add_item(self.valid_multimedia)
        self.catalog_manager1.add_item(self.valid_borrowed_multimedia)
        self.catalog_manager1.add_item(self.valid_overdue_multimedia)
        for item in [self.valid_overdue_Books, self.valid_overdue_multimedia]:
            self.assertIn(item, self.catalog_manager1.get_overdue_items())

    def test_get_overdue_fees(self):
        """ Get the total amount of overdue fee 090A """
        self.catalog_manager1.add_item(self.valid_Books)
        self.catalog_manager1.add_item(self.valid_borrowed_Books)
        self.catalog_manager1.add_item(self.valid_multimedia)
        self.catalog_manager1.add_item(self.valid_borrowed_multimedia)
        # 4611.0 is the initial overdue fees
        self.assertEqual(self.catalog_manager1.get_overdue_fees(), 0)
        self.catalog_manager1.add_item(self.valid_overdue_Books)
        self.catalog_manager1.add_item(self.valid_overdue_multimedia)
        self.assertEqual(self.catalog_manager1.get_overdue_fees(),
                         (datetime.date.today() - datetime.date(1999, 2, 3) - datetime.timedelta(4 * 7)).days * 0.3 * 2)

    def test_to_dict(self):
        """ Get a list of dictionary of the catalog """
        self.assertEqual(self.catalog_manager1.to_dict(), [])
        self.catalog_manager1.add_item(self.valid_Books)
        self.catalog_manager1.add_item(self.valid_borrowed_Books)
        self.catalog_manager1.add_item(self.valid_multimedia)
        self.catalog_manager1.add_item(self.valid_borrowed_multimedia)
        self.catalog_manager1.add_item(self.valid_overdue_Books)
        self.catalog_manager1.add_item(self.valid_overdue_multimedia)
        for i in [self.valid_Books, self.valid_borrowed_Books, self.valid_multimedia, self.valid_borrowed_multimedia,
                  self.valid_overdue_Books, self.valid_overdue_multimedia]:
            temp_dict = i.to_dict()
            # Only length become string
            temp_dict['length'] = str(temp_dict['length'])
            self.assertIn(temp_dict, self.catalog_manager1.to_dict())

    def test_add_json_books(self):
        """ Input a valid book in json format """
        self.catalog_manager1.add_item_from_json(
            {
                "author": "Eric K",
                "borrow_date": "2020-04-10",
                "genre": "informative",
                "is_borrowed": True,
                "isbn": 1234567891027,
                "length": "134",
                "pub_date": "2018-02-13",
                "publisher": "KE Publishing",
                "sub_type": "softcover",
                "title": "BCIT First look",
                "type_": "books"
            }
        )
        self.assertIn(self.valid_borrowed_Books, self.catalog_manager1.get_all_items())

    def test_add_json_multimedia(self):
        """ Input a valid multimedia in json format """
        self.catalog_manager1.add_item_from_json(
            {
                "author": "Eric K",
                "borrow_date": "2020-04-10",
                "genre": "informative",
                "is_borrowed": True,
                "isbn": 1234567891024,
                "length": "01:32:24",
                "pub_date": "2018-02-13",
                "publisher": "KE Publishing",
                "sub_type": "Bluray",
                "title": "BCIT First look",
                "type_": "multimedia"
            }
        )
        self.assertIn(self.valid_borrowed_multimedia, self.catalog_manager1.get_all_items())

    def test_get_stats(self):
        """ Get a CatalogState object 100A """
        self.assertIsInstance(self.catalog_manager1.get_stats(), CatalogStats)
        self.catalog_manager1.add_item(self.valid_Books)
        self.catalog_manager1.add_item(self.valid_borrowed_Books)
        self.catalog_manager1.add_item(self.valid_overdue_Books)
        self.catalog_manager1.add_item(self.valid_multimedia)
        self.catalog_manager1.add_item(self.valid_borrowed_multimedia)
        self.catalog_manager1.add_item(self.valid_overdue_multimedia)
        self.assertIsInstance(self.catalog_manager1.get_stats(), CatalogStats)

