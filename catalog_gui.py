# ACIT 2515: Assignment 4
# Author: Group 19
# catalog_gui.py

""" Library catalog GUI """

import tkinter as tk
from tkinter import ttk
import requests
from datetime import date
from add_book_popup import AddBookPopup
from add_multimedia_popup import AddMultimediaPopup
from remove_item_popup import RemoveItemPopup
from compute_stats_popup import ComputeStatsPopup


class MainAppController(tk.Frame):
    """ Main Application for GUI """

    def __init__(self, parent):
        """ Initialize Main Application """
        tk.Frame.__init__(self, parent)

        left_frame = ttk.Frame(master=self)
        left_frame.grid(row=1, column=1, sticky="N", padx='2m')

        right_frame = ttk.Frame(master=self)
        right_frame.grid(row=1, column=2, sticky="N")

        ttk.Label(left_frame, text="Library Catalog", font=("Verdana", 10,"bold"))\
            .grid(row=1, column=1, columnspan=3, ipady="2.4m")

        self._item_list = tk.Listbox(left_frame, height=13, width=20)
        self._item_list.grid(row=2, column=1, columnspan=3)

        self._item_list.bind("<<ListboxSelect>>", self._update_textbox)

        ttk.Button(left_frame, text="Add Book", command=self._add_book)\
            .grid(row=3, column=1, ipadx="1m", pady="1m", ipady="1m")
        ttk.Button(left_frame, text="Add Multimedia", command=self._add_multimedia)\
            .grid(row=3, column=3, ipadx="1m", pady="1m", ipady="1m")
        ttk.Button(left_frame, text="Remove Item", command=self._remove_item)\
            .grid(row=4, column=1, columnspan=3, ipadx="1m", pady="1m", ipady="1m")
        ttk.Button(self.master, text="Quit", command=self._quit_callback)\
            .pack(side=tk.BOTTOM, ipadx="1m", pady="1m", ipady="1m")

        tk.Label(right_frame, text="Item Information", font=("Verdana", 10, "bold"))\
            .grid(row=1, column=1, columnspan=2, ipady="2m")
        self._info_text = tk.Text(master=right_frame, height=13, width=40, font=("TkTextFont", 10), state="disabled")
        self._info_text.grid(row=2, column=1, columnspan=2)
        self._info_text.tag_configure("bold", font=("TkTextFont", 10, "bold"))
        ttk.Button(right_frame, text="Borrow", command=self._borrow_cb)\
            .grid(row=3, column=1, ipadx="1m", pady="1m", ipady="1m")
        ttk.Button(right_frame, text="Return", command=self._return_cb)\
            .grid(row=3, column=2, ipadx="1m", pady="1m", ipady="1m")
        # tk.Label(right_frame, text="").grid(row=3, column=1)
        ttk.Button(right_frame, text="Statistics", command=self._compute_stats)\
            .grid(row=4, column=1, columnspan=2, ipadx="1m", pady="1m", ipady="1m")

        self._update_item_list()

    def _update_textbox(self, evt):
        """ Updates the info text box on the right, based on the current ID selected """

        selected_values = self._item_list.curselection()
        if selected_values:
            selected_index = selected_values[0]
            isbn = self._item_list.get(selected_index)
        else:
            self._info_text["state"] = "normal"
            self._info_text.delete(1.0, tk.END)
            return

        r = requests.get("http://localhost:5000/catalogmanager/catalog/" + str(isbn))

        self._info_text["state"] = "normal"
        self._info_text.delete(1.0, tk.END)

        if r.status_code != 200:
            self._info_text.insert(tk.END, "Error running the request!")

        self._info_text["fg"] = "black"
        if r.content:
            for k, v in r.json().items():
                self._info_text.insert(tk.END, f"{k.capitalize()}\t\t", "bold")
                if k == "is_borrowed" and v:
                    self._info_text.insert(tk.END, f"{v}\n", "bold")
                    self._info_text["fg"] = "IndianRed4"
                elif r.json()["type_"] == 'books' and k == 'length':
                    self._info_text.insert(tk.END, f"{v} Pages\n")
                else:
                    self._info_text.insert(tk.END, f"{v}\n")
        self._info_text["state"] = "disabled"

    def _borrow_cb(self):
        """Borrow an item"""
        selected_values = self._item_list.curselection()
        selected_index = selected_values[0]
        isbn = self._item_list.get(selected_index)

        url = "http://localhost:5000/catalogmanager/catalog/" + str(isbn)
        r = requests.put(url, json={
            'operation': 'borrow',
            'date': date.strftime(date.today(), "%Y-%m-%d")
        })
        print(r.text)
        self._update_textbox("<<ListboxSelect>>")
        self._update_item_list()
        self._item_list.select_set(selected_index)

    def _return_cb(self):
        """Return an item"""
        selected_values = self._item_list.curselection()
        selected_index = selected_values[0]
        isbn = self._item_list.get(selected_index)

        url = "http://localhost:5000/catalogmanager/catalog/" + str(isbn)
        r = requests.put(url, json={
            'operation': 'return'
        })

        self._update_textbox("<<ListboxSelect>>")
        self._update_item_list()
        self._item_list.select_set(selected_index)

    def _compute_stats(self):
        """Compute library catalog statistics"""
        self._popup_win = tk.Toplevel()
        self._popup = ComputeStatsPopup(self._popup_win, self._close_popup_cb)

    def _remove_item(self):
        """Remove item from library catalog"""
        self._popup_win = tk.Toplevel()
        self._popup = RemoveItemPopup(self._popup_win, self._close_popup_cb)

    def _add_book(self):
        """ Add Book Popup """
        self._popup_win = tk.Toplevel()
        self._popup = AddBookPopup(self._popup_win, self._close_popup_cb)

    def _add_multimedia(self):
        """ Add Multimedia Popup """
        self._popup_win = tk.Toplevel()
        self._popup = AddMultimediaPopup(self._popup_win, self._close_popup_cb)

    def _close_popup_cb(self):
        """ Close Popup """
        self._popup_win.destroy()
        self._update_item_list()

    def _quit_callback(self):
        """ Quit """
        self.quit()

    def _update_item_list(self):
        """ Update the List of People """
        r = requests.get("http://localhost:5000/catalogmanager/catalog/all")
        self._item_list.delete(0, tk.END)
        for item in r.json():
            self._item_list.insert(tk.END, item['isbn'])


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x400")
    MainAppController(root).pack()
    root.mainloop()
