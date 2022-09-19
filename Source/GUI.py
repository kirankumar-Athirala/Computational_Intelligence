#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 22:59:54 2022

@author: kirankumarathirala
"""

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import sys
import os
import tkinter.scrolledtext as tkst
import subprocess
import re

root = Tk()
root.title("WLP")
root.geometry("975x475")
root.configure(bg='#0c0c0c')
root.resizable(0,0)



def clickstart():
     output = subprocess.run(['python', 'main.py'], stdout=subprocess.PIPE)
     output = str(output.stdout, encoding='utf-8')
     Textbox.insert(1.0, output)

Label1 = Label(root, text="WLP", bg="#0c0c0c", fg="#C0C0C0")
Label2 = Label(root, text="********************", 
bg="#0c0c0c", fg="#C0C0C0")
Label3 = Label(root, text="*********", bg="#0c0c0c", fg="#C0C0C0")
Button1 = Button(root, text="START", bg="#0c0c0c", fg="#C0C0C0", command=clickstart)  #)
Textbox = tkst.ScrolledText(root, width=85, height=10, bg="#0c0c0c", fg="#C0C0C0")

Label1.grid(row=5, column=5, pady=15)
Label2.grid(row=7, column=5, pady=15)
Label3.grid(row=85, column=0, pady=125)
Button1.grid(row=10, column=5, pady=15)
Textbox.grid(row=17, column=5)

root.mainloop()