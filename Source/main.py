#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 17:42:30 2022

@author: kirankumarathirala
"""

import argparse
import sys
# Import all components from tkinter library for simple GUI
import tkinter as tk
from tkinter import filedialog
import pandas as pd

def Process_CSV_Data(data_file):
    ##todo
    print("todo")
























if __name__ == '__main__':
    
    process_data_file = None
    
    if (len(sys.argv) == 1):
        parser = argparse.ArgumentParser(description="data file")
        parser.add_argument('--input_file', required=False, help="input file containing training data (csv)")
        args = parser.parse_args()
        
        if args.input_file is not None:
            process_data_file = args.input_file
        
    else:
        print("Invalid number of arguments. It accepts only one argument, which is input_file")
        sys.exit()
    if process_data_file is None:
        
        try:
        
           root = tk.Tk()
           root.wm_withdraw()
        
           process_data_file = filedialog.askopenfilename(initialdir = "/",
                                         filetypes = (("xlsx files",
                                                       "*.xlsx*"),
                                                      ("all files",
                                                       "*.*")),
                                         title = "Choose Training CSV File.")
           root.update()
           root.destroy()
           root.mainloop()
           Process_CSV_Data(process_data_file)
        except Exception as ex:
            print("Exception",ex)
        
            
        
        
    