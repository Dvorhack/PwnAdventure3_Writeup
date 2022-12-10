#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Authors: Dvorhack & K8pl3r

GUI for cheet tools
"""

from tkinter import *
import customtkinter
import importlib
import Protocol_Parser

class LogFrame(customtkinter.CTkFrame):
    """Frame for logs"""
    def __init__(self, *args, header_name="RadioButtonFrame", **kwargs):
        super().__init__(*args, **kwargs)

        self.activate_filter = False

        self.header_name = header_name

        self.header = customtkinter.CTkLabel(self, text=self.header_name)

        # create 2x2 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0), weight=1)

        # Textbox for displaying logs
        self.textbox = customtkinter.CTkTextbox(master=self)
        self.textbox.grid(row=0, column=0, columnspan=3, padx=10, pady=(20, 0), sticky="nsew")

        # Combobox for defautl filters
        self.combobox = customtkinter.CTkComboBox(master=self, values=Protocol_Parser.FILTERS)
        self.combobox.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Button for filtering
        self.button = customtkinter.CTkButton(master=self, command=self.button_callback, text="Filter down", fg_color="red", hover=False)
        self.button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Button activate filter / reload filters
        self.active_filter_button = customtkinter.CTkButton(master=self, command=self.active_filter_callback, text="Reload filters")
        self.active_filter_button.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

    def button_callback(self):
        """Callback when button pressed"""
        self.textbox.insert("insert", self.combobox.get() + "\n")
        if self.activate_filter:
            self.button.configure(fg_color="red", text="Filter down")
            self.activate_filter = False
        else:
            self.button.configure(fg_color="green", text="Filter activated")
            self.activate_filter = True
    
    def active_filter_callback(self):
        """Activate filter callback"""
        importlib.reload(Protocol_Parser)
        self.combobox.configure(values=Protocol_Parser.FILTERS)
        self.combobox.set(Protocol_Parser.FILTERS[0])

class CmdInput(customtkinter.CTkFrame):
    """Frame for logs"""
    def __init__(self, *args, header_name="RadioButtonFrame", **kwargs):
        super().__init__(*args, **kwargs)

        self.header_name = header_name

        self.header = customtkinter.CTkLabel(self, text=self.header_name)

        self.entry = customtkinter.CTkEntry(master=self, placeholder_text="CTkEntry")
        self.entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.button = customtkinter.CTkButton(master=self, command=self.button_callback, text="Insert Text")
        self.button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    def button_callback(self):
        """Callback when button pressed"""
        print("insert", self.entry.get() + "\n")

class MainWin(customtkinter.CTk):
    """
    Main window
    """
    def __init__(self):
        super().__init__()

        self.geometry("800x600")
        self.title("Cheat Tools")
        self.minsize(300, 200)
        self.state('zoomed')

        # Create 2X1 grid
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.log_frame = LogFrame(self, header_name="RadioButtonFrame 1")
        self.log_frame.grid(row=0, rowspan=2,column=1, sticky="nsew")

        self.cmd_input = CmdInput(self, header_name="RadioButtonFrame 1")
        self.cmd_input.grid(row=0, rowspan=2,column=0)

        print(self.grid_size())
