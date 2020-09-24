# ACIT 2515: Assignment 4
# Author: Group 19
# compute_stats_popup.py

""" Popup to compute the library catalog statistics """

import requests
import tkinter as tk
from tkinter import ttk, messagebox


class ComputeStatsPopup(tk.Frame):
    """ Popup Frame to compute library catalog statistics """

    def __init__(self, parent, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self.grid(rowspan=3, columnspan=2)

        ttk.Label(self, text="Library Catalog Statistics", font=("Verdana", 15, "bold")).grid(row=1, column=1)
        self._stats_text = tk.Text(self, height=10, width=50)
        self._stats_text.grid(row=2, column=1)

        self._update_stats_text()

    def _update_stats_text(self):
        """ Update the statistics textbox """
        r = requests.get("http://localhost:5000/catalogmanager/catalog/stats")
        if r.status_code != 200:
            messagebox.showerror(title="Error", message="Error running the request!")

        self._stats_text.insert(tk.END, "Number of books: ")
        self._stats_text.insert(tk.END, r.json()["num_books"])
        self._stats_text.insert(tk.END, "\nNumber of multimedia: ")
        self._stats_text.insert(tk.END, r.json()["num_media"])
        self._stats_text.insert(tk.END, "\nNumber of borrowed items: ")
        self._stats_text.insert(tk.END, r.json()["num_borrowed"])
        self._stats_text.insert(tk.END, "\nNumber of available items: ")
        self._stats_text.insert(tk.END, r.json()["num_available"])
        self._stats_text.insert(tk.END, "\nNumber of overdue items: ")
        self._stats_text.insert(tk.END, r.json()["num_overdue"])
        self._stats_text.insert(tk.END, "\nTotal fees: $")
        self._stats_text.insert(tk.END, r.json()["total_fees"])
