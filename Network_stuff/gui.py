#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Authors: Dvorhack & K8pl3r

GUI for cheet tools
"""

from tkinter import *
import customtkinter

class LogFrame(customtkinter.CTkFrame):
    """Frame for logs"""
    def __init__(self, *args, header_name="RadioButtonFrame", **kwargs):
        super().__init__(*args, **kwargs)

        self.header_name = header_name

        self.header = customtkinter.CTkLabel(self, text=self.header_name)

        # create 2x2 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)


        self.textbox = customtkinter.CTkTextbox(master=self)
        self.textbox.grid(row=0, column=0, columnspan=2, padx=10, pady=(20, 0), sticky="nsew")

        self.combobox = customtkinter.CTkComboBox(master=self, values=["Sample text 1", "Text 2"])
        self.combobox.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.button = customtkinter.CTkButton(master=self, command=self.button_callback, text="Insert Text")
        self.button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    def button_callback(self):
        """Callback when button pressed"""
        self.textbox.insert("insert", self.combobox.get() + "\n")

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

        # Create 2X1 grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.log_frame = LogFrame(self, header_name="RadioButtonFrame 1", bg_color="red")
        self.log_frame.grid(row=0, rowspan=2,column=1)

        self.cmd_input = CmdInput(self, header_name="RadioButtonFrame 1")
        self.cmd_input.grid(row=0, rowspan=2,column=0)

        print(self.grid_size())
