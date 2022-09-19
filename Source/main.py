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
    lag = 3400
    threshold = 12
    influence = 0.3
    # Run algo with settings from above
    result = init(data[0], lag=lag, threshold=threshold, influence=influence)
    # Plot result
    pylab.subplot(211)
    pylab.plot(np.arange(1, len(data[0]) + 1), data[0])
    pylab.subplot(212)
    pylab.step(np.arange(1, len(data[0]) + 1), result['labels'], color='red',
           lw=2)
    pylab.ylim(-1.5, 1.5)
    pylab.show()
def init(x,lag,threshold,influence,):
    '''
    Smoothed z-score algorithm
    Implementation of algorithm from https://stackoverflow.com/a/22640362/6029703
    '''

    labels = np.zeros(lag)
    filtered_y = np.array(x[0:lag])
    avg_filter = np.zeros(lag)
    std_filter = np.zeros(lag)
    var_filter = np.zeros(lag)

    avg_filter[lag - 1] = np.mean(x[0:lag])
    std_filter[lag - 1] = np.std(x[0:lag])
    var_filter[lag - 1] = np.var(x[0:lag])

    return dict(avg=avg_filter[lag - 1], var=var_filter[lag - 1],
                std=std_filter[lag - 1], filtered_y=filtered_y,
                labels=labels)

def add(result,single_value,lag,threshold,influence,):
    previous_avg = result['avg']
    previous_var = result['var']
    previous_std = result['std']
    filtered_y = result['filtered_y']
    labels = result['labels']

    if abs(single_value - previous_avg) > threshold * previous_std:
        if single_value > previous_avg:
            labels = np.append(labels, 1)
        else:
            labels = np.append(labels, -1)

        # calculate the new filtered element using the influence factor
        filtered_y = np.append(filtered_y, influence * single_value
                               + (1 - influence) * filtered_y[-1])
    else:
        labels = np.append(labels, 0)
        filtered_y = np.append(filtered_y, single_value)

    # update avg as sum of the previuos avg + the lag * (the new calculated item - calculated item at position (i - lag))
    current_avg_filter = previous_avg + 1. / lag * (filtered_y[-1]
            - filtered_y[len(filtered_y) - lag - 1])

    # update variance as the previuos element variance + 1 / lag * new recalculated item - the previous avg -
    current_var_filter = previous_var + 1. / lag * ((filtered_y[-1]
            - previous_avg) ** 2 - (filtered_y[len(filtered_y) - 1
            - lag] - previous_avg) ** 2 - (filtered_y[-1]
            - filtered_y[len(filtered_y) - 1 - lag]) ** 2 / lag)  # the recalculated element at pos (lag) - avg of the previuos - new recalculated element - recalculated element at lag pos ....

    # calculate standard deviation for current element as sqrt (current variance)
    current_std_filter = np.sqrt(current_var_filter)

    return dict(avg=current_avg_filter, var=current_var_filter,
                std=current_std_filter, filtered_y=filtered_y[1:],
                labels=labels)


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
        
            
        
        
    