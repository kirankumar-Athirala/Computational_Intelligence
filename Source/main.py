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
import numpy as np
import pylab
import subprocess
import threading
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft

def Process_CSV_Data(data_file):
    
    csv_data = pd.read_excel(data_file,header=None)
    singal_data = []
    for i in range(0, len(csv_data.index)):
        try: 
            singal_data.append(csv_data.iloc[i , 6:]) 
        except Exception as ex:
            print("Exception",ex)
    return singal_data

def peekdetection(data):
    lag = 30
    threshold = 5
    influence = 10
    y = data[0]
    result = thresholding_algo(y, lag=lag, threshold=threshold, influence=influence)

# Plot result
    pylab.subplot(211)
    pylab.plot(np.arange(1, len(y)+1), y)

    pylab.plot(np.arange(1, len(y)+1),
           result["avgFilter"], color="cyan", lw=2)

    pylab.plot(np.arange(1, len(y)+1),
           result["avgFilter"] + threshold * result["stdFilter"], color="green", lw=2)

    pylab.plot(np.arange(1, len(y)+1),
           result["avgFilter"] - threshold * result["stdFilter"], color="green", lw=2)

    pylab.subplot(212)
    pylab.step(np.arange(1, len(y)+1), result["signals"], color="red", lw=2)
    pylab.ylim(-1.5, 1.5)
    pylab.show()
    
def thresholding_algo(y, lag, threshold, influence):
    signals = np.zeros(len(y))
    filteredY = np.array(y)
    avgFilter = [0]*len(y)
    stdFilter = [0]*len(y)
    avgFilter[lag - 1] = np.mean(y[0:lag])
    stdFilter[lag - 1] = np.std(y[0:lag])
    for i in range(lag, len(y)):
        if abs(y[i] - avgFilter[i-1]) > threshold * stdFilter [i-1]:
            if y[i] > avgFilter[i-1]:
                signals[i] = 1
            else:
                signals[i] = -1

            filteredY[i] = influence * y[i] + (1 - influence) * filteredY[i-1]
            avgFilter[i] = np.mean(filteredY[(i-lag+1):i+1])
            stdFilter[i] = np.std(filteredY[(i-lag+1):i+1])
        else:
            signals[i] = 0
            filteredY[i] = y[i]
            avgFilter[i] = np.mean(filteredY[(i-lag+1):i+1])
            stdFilter[i] = np.std(filteredY[(i-lag+1):i+1])

    return dict(signals = np.asarray(signals),
                avgFilter = np.asarray(avgFilter),
                stdFilter = np.asarray(stdFilter))


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
           peekdetection(signal_data)
           

        except Exception as ex:
            print("Exception",ex)
        
            
        
        
    