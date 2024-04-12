#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 3/21/24 
# @Author  : Marieke Louage, Xiaoke Wang
# @Group   : UGent HES
# @File    : readvpr.py
# @Software: PyCharm, Ghent


import os
import re
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sys
import csv
import pandas as pd
import numpy as np


def parse_log_file(filepath):
    with open(filepath, 'r') as file:
        content = file.read()

    time_regex = r"The entire flow of VPR took ([\d.]+) seconds"
    cpd_regex = r"Final critical path delay \(least slack\): ([\d.]+) ns, Fmax: ([\d.]+) MHz"
    wirelength_regex = r"Total wirelength: ([\d]+), average net length: ([\d.]+)"

    time = re.search(time_regex, content)
    cpd = re.search(cpd_regex, content)
    wirelength = re.search(wirelength_regex, content)

    return {
        "time": float(time.group(1)) if time else None,
        "cpd": float(cpd.group(1)) if cpd else None,
        "fmax": float(cpd.group(2)) if cpd else None,
        "total_wirelength": int(wirelength.group(1)) if wirelength else None,
        "average_net_length": float(wirelength.group(2)) if wirelength else None
    }


def extract_rent_exponent(filename):
    match = re.search(r"rent_exp_([0-9.]*[0-9])", filename)
    return float(match.group(1)) if match else None



def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def fit_and_plot_exponential(filename, columns_to_fit):
    data = pd.read_csv(filename)

    def exponential_func(x, a, b, c):
        return a * np.exp(-b * x) + c

    fitted_parameters = {}
    for column in columns_to_fit:
        # Sort the data points based on the "rent_value" column
        sorted_data = data.sort_values(by='rent_exp')
        clean_data = sorted_data.dropna(subset=[column])

        if clean_data.empty:
            print(f"Warning: No data available for column '{column}' in file '{filename}'")
            continue

        try:
            popt, _ = curve_fit(exponential_func, clean_data['rent_exp'], clean_data[column])
            fitted_parameters[column] = popt
        except RuntimeError:
            print(f"Error: Unable to fit exponential curve for column '{column}' in file '{filename}'")
            continue
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    num_plots = len(fitted_parameters)
    fig, axs = plt.subplots(num_plots, 1, figsize=(10, 6 * num_plots))

    for i, (column, popt) in enumerate(fitted_parameters.items()):
        fitted_values = exponential_func(clean_data['rent_exp'], *popt)  # Use clean_data here
        axs[i].scatter(clean_data['rent_exp'], clean_data[column], label=f'Original {column}', color=colors[i])  # Use clean_data here
        axs[i].plot(clean_data['rent_exp'], fitted_values, label=f'Fitted {column}', color=colors[i],  linewidth=3, alpha=0.7)
        axs[i].set_xlabel('Rent Exponent')
        axs[i].set_ylabel('Value')
        axs[i].set_title(f'Exponential Fit for {column}')
        axs[i].legend()
        axs[i].grid(True)

    plt.tight_layout()
    directory = os.path.dirname(filename)
    plt.savefig(os.path.join(directory, 'rent_exp_influence2vpr_flow.png'))
    plt.show()



if __name__ == '__main__':

    #    log_folder = "./sweep/vpr_files"
    if len(sys.argv) != 3:
        print("Usage: python analyze_vpr_logs.py <log_folder> <output_figures_folder>")
        sys.exit(1)

    log_folder = sys.argv[1]
    output_figures_folder = sys.argv[2]

    log_files = [os.path.join(root, f)
                 for root, dirs, files in os.walk(log_folder)
                 for f in files if f == "vpr_stdout.log"]

    data = []
    for filepath in log_files:
        log_data = parse_log_file(filepath)
        rent_exp = extract_rent_exponent(filepath)
        log_data["rent_exp"] = rent_exp
        data.append(log_data)

    # rent_exps = [d["rent_exp"] for d in data]
    # cpds = [d["cpd"] for d in data]
    # times = [d["time"] for d in data]
    # total_wirelengths = [d["total_wirelength"] for d in data]

    csv_filename = os.path.join(output_figures_folder, 'vpr_data.csv')
    save_to_csv(data, csv_filename)
    fit_and_plot_exponential(csv_filename, columns_to_fit = ['time', 'cpd', 'total_wirelength'])
