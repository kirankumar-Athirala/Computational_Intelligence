#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 21:14:52 2022

@author: kirankumarathirala
"""

import numpy as np
import matplotlib.pyplot as plt 
from scipy.signal import find_peaks
import argparse
import sys
# Import all components from tkinter library for simple GUI
import tkinter as tk
from tkinter import filedialog
import pandas as pd

def Process_CSV_Data(data_file):
    
    csv_data = pd.read_excel(data_file,header=None)
    singal_data = []
    for i in range(0, len(csv_data.index)):
        try: 
            singal_data.append(csv_data.iloc[i , 6:]) 
        except Exception as ex:
            print("Exception",ex)
    return singal_data

if __name__ == '__main__':
    
    process_data_file = None
    
    if (len(sys.argv) == 1):
        parser = argparse.ArgumentParser(description="less script")
        parser.add_argument('--input_file', required=False, help="input file containing IDs and attributes to change (csv)")
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
                                         filetypes = (("CSV files",
                                                       "*.xlsx*"),
                                                      ("all files",
                                                       "*.*")),
                                         title = "Choose Training CSV File.")
           root.update()
           root.destroy()
           root.mainloop()
           signal_data = Process_CSV_Data(process_data_file)
           

        except Exception as ex:
            print("Exception",ex)
        
    x =signal_data[0]
    peaks, _ = find_peaks(x, distance=20)
    peaks2, _ = find_peaks(x, prominence=1)      # BEST!
    peaks3, _ = find_peaks(x, width=20)
    peaks4, _ = find_peaks(x, threshold=0.4)     # Required vertical distance to its direct neighbouring samples, pretty useless
    plt.subplot(2, 2, 1)
    plt.plot(peaks, x[peaks], "xr"); plt.plot(x); plt.legend(['distance'])
    plt.subplot(2, 2, 2)
    plt.plot(peaks2, x[peaks2], "XR"); plt.plot(x); plt.legend(['prominence'])
    plt.subplot(2, 2, 3)
    plt.plot(peaks3, x[peaks3], "vg"); plt.plot(x); plt.legend(['width'])
    plt.subplot(2, 2, 4)
    plt.plot(peaks4, x[peaks4], "xk"); plt.plot(x); plt.legend(['threshold'])
    plt.show()