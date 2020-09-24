from catalog_manager import CatalogManager
from multimedia import Multimedia
from books import Books
import datetime

if __name__ == "__main__":
    catalog_manager1 = CatalogManager("Catalog1")
    valid_multimedia = Multimedia(isbn=1234567891023, author="Eric N", publisher="BE Publishing", title="1000 night at school",
                                       genre="romantic", pub_date=datetime.date(2020, 1, 30), length="01:32:24", sub_type="CD", type_="multimedia")
    valid_borrowed_multimedia = Multimedia(isbn=1234567891024, author="Eric K", publisher="KE Publishing", title="BCIT First look",
                                                genre="informative", pub_date=datetime.date(2018, 2, 13), length="01:32:24", sub_type="Bluray", type_="multimedia")
    valid_borrowed_multimedia.borrow(datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m-%d"))
    valid_overdue_multimedia = Multimedia(isbn=1234567891025, author="Eric W", publisher="CA Publishing", title="Fairies",
                                               genre="romantic", pub_date=datetime.date(1998, 1, 30), length="01:32:24", sub_type="VHS", type_="multimedia")
    valid_overdue_multimedia.borrow("1999-02-03")
    valid_Books = Books(isbn=1234567891026, author="Eric N", publisher="BE Publishing", title="1000 night at school",
                             genre="romantic", pub_date=datetime.date(2020, 1, 30), length=324, sub_type="hardcover", type_="books")
    valid_borrowed_Books = Books(isbn=1234567891027, author="Eric K", publisher="KE Publishing", title="BCIT First look",
                                      genre="informative", pub_date=datetime.date(2018, 2, 13), length=134, sub_type="softcover", type_="books")
    valid_borrowed_Books.borrow(datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m-%d"))
    valid_overdue_Books = Books(isbn=1234567891028, author="Eric W", publisher="CA Publishing", title="Fairies",
                                     genre="romantic", pub_date=datetime.date(1998, 1, 30), length=688, sub_type="softcover", type_="books")
    valid_overdue_Books.borrow("1999-02-03")
    # print(valid_Books.get_details())
    # print(valid_borrowed_Books.get_details())
    # print(valid_overdue_Books.get_details())
    # print(valid_multimedia.get_details())
    # print(valid_borrowed_multimedia.get_details())
    # print(valid_overdue_multimedia.get_details())

    catalog_manager1.add_item(valid_Books)
    catalog_manager1.add_item(valid_borrowed_Books)
    catalog_manager1.add_item(valid_overdue_Books)
    catalog_manager1.add_item(valid_multimedia)
    catalog_manager1.add_item(valid_borrowed_multimedia)
    catalog_manager1.add_item(valid_overdue_multimedia)

    # stat = catalog_manager1.get_stats()
    # print("Number of items available:", stat.get_num_available())
    # print("Number of books:", stat.get_num_books())
    # print("Number of borrowed items", stat.get_num_borrowed())
    # print("Number of Media", stat.get_num_media())
    # print("Number of overdued items:", stat.get_num_overdue())
    # print("Total receivable fee: $", stat.get_total_fees())
    # input("")
    # catalog_manager1.delete_item_by_isbn(1234567891027)