# ACIT 2515: Assignment 4
# Author: Group 19
# remove_item_popup.py

""" Popup to remove an item from the library catalog """

import requests
import tkinter as tk
from tkinter import ttk, messagebox


class RemoveItemPopup(tk.Frame):
    """ Popup Frame to Remove an item """

    def __init__(self, parent, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self.grid(rowspan=3, columnspan=2, padx="2m", pady="2m")

        ttk.Label(self, text="ISBN:").grid(row=1, column=1)
        self._isbn = ttk.Entry(self)
        self._isbn.grid(row=1, column=2)

        self._info_label = ttk.Label(self, text="")
        self._info_label.grid(row=3, column=1, columnspan=2)

        ttk.Button(self, text="Submit", command=self._submit_cb)\
            .grid(row=2, column=1, columnspan=2, ipadx="2m", ipady="2m", pady="2m")

    def _submit_cb(self):
        """ Remove the person from the people list """
        message = "Remove item: " + self._isbn.get() + "?"

        if self._isbn.get().isdigit() and (len(self._isbn.get()) == 10 or len(self._isbn.get()) == 13):
            url = "http://localhost:5000/catalogmanager/catalog/" + self._isbn.get()
            get_response = requests.get(url)
            if get_response.status_code == 200:
                choice = messagebox.askokcancel(title="Confirm Submission", message=message)
                if choice:
                    delete_response = requests.delete(url)
                    print(delete_response.text)
                    self._close_cb()
            else:
                text = "Item " + self._isbn.get() + " is not in the library catalog."
                self._info_label.config(text=text)
        else:
            self._info_label.config(text="Invalid ISBN. Must be 10 or 13 digits.")
