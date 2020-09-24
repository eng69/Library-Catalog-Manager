# ACIT 2515: Assignment 4
# Author: Group 19
# add_multimedia_popup.py

""" Popup to add multimedia to the library catalog """

import requests
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox


class AddMultimediaPopup(tk.Frame):
    """ Popup Frame to Add Multimedia """

    def __init__(self, parent, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2, padx="2m", pady="2m")

        ttk.Label(self, text="ISBN:").grid(row=1, column=1)
        self._isbn = ttk.Entry(self)
        self._isbn.grid(row=1, column=2)
        ttk.Label(self, text="Author:").grid(row=2, column=1)
        self._author = ttk.Entry(self)
        self._author.grid(row=2, column=2)
        ttk.Label(self, text="Publisher:").grid(row=3, column=1)
        self._publisher = ttk.Entry(self)
        self._publisher.grid(row=3, column=2)
        ttk.Label(self, text="Title:").grid(row=4, column=1)
        self._title = ttk.Entry(self)
        self._title.grid(row=4, column=2)
        ttk.Label(self, text="Genre:").grid(row=5, column=1)
        self._genre = ttk.Entry(self)
        self._genre.grid(row=5, column=2)
        ttk.Label(self, text="Publish Date:").grid(row=6, column=1)
        self._pub_date = ttk.Entry(self)
        self._pub_date.grid(row=6, column=2)
        ttk.Label(self, text="Borrowed?:").grid(row=7, column=1)
        self._is_borrowed = ttk.Entry(self)
        self._is_borrowed.grid(row=7, column=2)
        ttk.Label(self, text="Borrow Date:").grid(row=8, column=1)
        self._borrow_date = ttk.Entry(self)
        self._borrow_date.grid(row=8, column=2)
        ttk.Label(self, text="Length (time):").grid(row=9, column=1)
        self._length = ttk.Entry(self)
        self._length.grid(row=9, column=2)
        ttk.Label(self, text="Media Type:").grid(row=10, column=1)
        self._sub_type = ttk.Entry(self)
        self._sub_type.grid(row=10, column=2)
        ttk.Button(self, text="Close", command=self._close_cb)\
            .grid(row=11, column=1, pady="2m", ipadx="1m", ipady="1m")
        ttk.Button(self, text="Submit", command=self._submit_cb)\
            .grid(row=11, column=2, pady="2m", ipadx="1m", ipady="1m")

    def _submit_cb(self):
        """ Submit the book """
        data = {}
        error_msgs = []

        # Invalid entry checks
        if not self._isbn.get().isdigit() and not (len(self._isbn.get()) == 10 or len(self._isbn.get()) == 13):
            error_msgs.append("Invalid ISBN. Must be 10 or 13 digits.")
        r = requests.get("http://localhost:5000/catalogmanager/catalog/" + str(self._isbn.get().strip()))
        if r.status_code == 200:
            error_msgs.append("Item with the same ISBN exist.")
        if self._author.get().strip() == "":
            error_msgs.append("Invalid author name.")
        if self._publisher.get().strip() == "":
            error_msgs.append("Invalid publisher.")
        if self._title.get().strip() == "":
            error_msgs.append("Invalid title.")
        if self._genre.get().strip() == "":
            error_msgs.append("Invalid genre.")
        try:
            ok_pdate = True
            datetime.strptime(self._pub_date.get(), "%Y-%m-%d")
        except:
            ok_pdate = False
        if not ok_pdate:
            error_msgs.append("Invalid publish date. Publish date should be in YYYY-MM-DD format")
        try:
            ok_bdate = True
            datetime.strptime(self._borrow_date.get(), "%Y-%m-%d")
        except:
            ok_bdate = False
        if self._is_borrowed.get().strip().lower() not in ("yes", "no", ""):
            error_msgs.append("Invalid borrowed state. Must be yes/no or blank.")
        if self._is_borrowed.get().strip().lower() in ("no", ""):
            ok_bdate = True
        if not ok_bdate:
            error_msgs.append("Invalid borrow date. Borrow date should be in YYYY-MM-DD format")
        try:
            ok_length = True
            datetime.strptime(self._length.get().strip(), "%H:%M:%S")
        except:
            ok_length = False
        if not ok_length:
            error_msgs.append("Invalid multimedia length. Media Length should be in HH:MM:SS format")
        if self._sub_type.get().strip() == "":
            error_msgs.append("Invalid multimedia type.")

        # Display error or success message
        if len(error_msgs) > 0:
            messagebox.showerror(title="Entry error", message="\n".join(error_msgs))
            return

        # Populate data dictionary
        data['isbn'] = self._isbn.get()
        data['author'] = self._author.get()
        data['publisher'] = self._publisher.get()
        data['title'] = self._title.get()
        data['genre'] = self._genre.get()
        data['pub_date'] = self._pub_date.get()
        data['is_borrowed'] = self._is_borrowed.get()
        data['borrow_date'] = self._borrow_date.get()
        data['length'] = self._length.get()
        data['sub_type'] = self._sub_type.get()
        data['type_'] = "multimedia"

        r = requests.post("http://localhost:5000/catalogmanager/catalog", json=data)
        print(r.text)
        if r.status_code == 200:
            messagebox.showinfo(title="Entry successful", message="Multimedia added to the library catalog!")
            self._close_cb()
        else:
            print()
            messagebox.showinfo(title="Entry unsuccessful", message="Oops, something went wrong!")