#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/8/24 
# @Author  : Xiaoke Wang
# @Group   : UGent HES
# @File    : compvpr.py
# @Software: PyCharm, Ghent

import os
import re
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sys
import csv
import pandas as pd
import numpy as np


# def draw_fit_in_diff_files(filenames, columns_to_fit, rent_length=None):
#     def exponential_func(x, a, b, c):
#         return a * np.exp(-b * x) + c
#
#     fig, axs = plt.subplots(len(columns_to_fit), 1, figsize=(10, 6 * len(columns_to_fit)))
#     plt.rcParams['text.usetex'] = True
#     if not isinstance(axs, np.ndarray):
#     	axs = [axs]
#     for i, column in enumerate(columns_to_fit):
#         colors = [
#             '#1f77b4',  # muted blue
#             '#ff7f0e',  # safety orange
#             '#2ca02c',  # cooked asparagus green
#             '#d62728',  # brick red
#             '#9467bd',  # muted purple
#             '#8c564b',  # chestnut brown
#             '#e377c2',  # raspberry yogurt pink
#             '#7f7f7f',  # middle gray
#             '#bcbd22',  # curry yellow-green
#             '#17becf'  # blue-teal
#         ]
#
#         fitted_values_region = []
#         rent_exp = []
#
#         for j, filename in enumerate(filenames):
#             data = pd.read_csv(filename)
#             sorted_data = data.sort_values(by='rent_exp')
#             clean_data = sorted_data.dropna(subset=[column])
#             numbers = re.findall(r'\d+', os.path.basename(filename))
#             rent_exp.append(clean_data['rent_exp'].values)
#             if numbers:
#                 number = numbers[0]  # Use the first number found
#             else:
#                 number = os.path.basename(filename)
#             if clean_data.empty:
#                 print(f"Warning: No data available for column '{column}' in file '{filename}'")
#                 continue
#
#             try:
#                 if rent_length is not None:
#                     popt, _ = curve_fit(exponential_func, clean_data['rent_exp'].iloc[:rent_length], clean_data[column].iloc[:rent_length])
#                     fitted_values = exponential_func(clean_data['rent_exp'].iloc[:rent_length], *popt)
#
#                     # Store the fitted values for each curve separately
#                     fitted_values_region.append(fitted_values)
#
#                     a, b, c = popt
#
#                     label = f'Blocks: {number}\nFit: $y = ({a:.2e}) \\cdot \\exp({-b:.2f}  x) + {c:.2f}$'
#
#                     axs[i].scatter(clean_data['rent_exp'].values[:rent_length], clean_data[column].values[:rent_length], label=label, color=colors[j % len(colors)])
#                     axs[i].plot(clean_data['rent_exp'].values[:rent_length], fitted_values.values, color=colors[j % len(colors)], linewidth=3, alpha=0.7)
#                 else:
#                     popt, _ = curve_fit(exponential_func, clean_data['rent_exp'], clean_data[column])
#                     fitted_values = exponential_func(clean_data['rent_exp'], *popt)
#
#                     # Store the fitted values for each curve separately
#                     fitted_values_region.append(fitted_values)
#
#                     a, b, c = popt
#                     label = f'Blocks: {number}\nFit: $y = ({a:.4f}) \\cdot e^{-b:.2f \\cdot x} + {c:.2f}$'
#                     axs[i].scatter(clean_data['rent_exp'].values, clean_data[column].values, label=label, color=colors[j % len(colors)])
#                     axs[i].plot(clean_data['rent_exp'].values, fitted_values.values, color=colors[j % len(colors)], linewidth=3, alpha=0.7)
#
#             except RuntimeError:
#                 print(f"Error: Unable to fit exponential curve for column '{column}' in file '{filename}'")
#                 continue
#
#         if fitted_values_region:
#             shortest_length = min(len(values) for values in fitted_values_region)
#             print(f"shot length: {shortest_length}")
#             if rent_length is not None and rent_length <= shortest_length:
#                 shortest_length = rent_length
#         else:
#             print("Not enough data points were successfully fitted to compare lengths.")
#             shortest_length = None
#         resized_fitted_values = []
#
#         for values in fitted_values_region:
#             resized_values = values[:shortest_length] # Keep only the first 'shortest_length' elements
#             resized_fitted_values.append(resized_values)
#         print(resized_fitted_values)
#         for k in range(len(resized_fitted_values) - 1):
#             axs[i].fill_between( max(rent_exp, key=len)[:shortest_length], resized_fitted_values[k], resized_fitted_values[k-1],
#                                 color=colors[k], alpha=0.3)
#
#         axs[i].set_xlabel('Rent Exponent')
#         axs[i].set_ylabel('Value')
#         axs[i].set_title(f'Exponential Fit for {column}')
#         axs[i].legend()
#         axs[i].grid(True)
#
#     plt.tight_layout()
#     directory = os.path.dirname(filenames[0])  # Use the directory of the first file for saving the plot
#     plt.savefig(os.path.join(directory, 'rent_exp_influence2vpr_flow.png'))
#
#     plt.show()


def draw_fit_in_diff_files(filenames, columns_to_fit, rent_length=None):
    def exponential_func(x, a, b, c):
        return a * np.exp(b * x) + c

    sorted_filenames = sorted(filenames, key=extract_number)

    fig, axs = plt.subplots(len(columns_to_fit), 1, figsize=(10, 6 * len(columns_to_fit)))
    plt.rcParams.update({
        "text.usetex": True,
        "text.latex.preamble": r"\usepackage{xcolor}"
    })
    if not isinstance(axs, np.ndarray):
        axs = [axs]

    # Create a colormap instance
    cmap = plt.colormaps.get_cmap('Set1')  # 'viridis' with as many colors as there are files

    for i, column in enumerate(columns_to_fit):
        fitted_values_region = []
        rent_exp = []

        for j, filename in enumerate(sorted_filenames):
            data = pd.read_csv(filename)
            sorted_data = data.sort_values(by='rent_exp')
            clean_data = sorted_data.dropna(subset=[column])
            numbers = re.findall(r'\d+', os.path.basename(filename))
            rent_exp.append(clean_data['rent_exp'].values)
            number = numbers[0] if numbers else os.path.basename(filename)
            if clean_data.empty:
                print(f"Warning: No data available for column '{column}' in file '{filename}'")
                continue

            if rent_length is not None:
                rent_exp_data = clean_data['rent_exp'].values[:rent_length]
                clean_data_value = clean_data[column].values[:rent_length]
            else:
                rent_exp_data = clean_data['rent_exp'].values
                clean_data_value = clean_data[column].values
            axs[i].scatter(rent_exp_data, clean_data_value, color=cmap(j))
            try:
                if rent_length is not None:
                    popt, _ = curve_fit(exponential_func, clean_data['rent_exp'].iloc[:rent_length],
                                        clean_data[column].iloc[:rent_length])
                    fitted_values = exponential_func(clean_data['rent_exp'].iloc[:rent_length], *popt)
                else:
                    popt, _ = curve_fit(exponential_func, clean_data['rent_exp'], clean_data[column])
                    fitted_values = exponential_func(clean_data['rent_exp'], *popt)

                fitted_values_region.append(fitted_values)

                a, b, c = popt
                a_sci = f"{a:.2e}".split('e')  # 分解为基数和指数
                a_base, a_exp = a_sci[0], a_sci[1]
                # label = f'Blocks: {number}\nFit: $y = ({a:.2e}) \\cdot e^{{-b:.2f \\cdot x}} + {c:.2f}$'
                label = f'Blocks: ${number}$\n Fit: $y =  ({a_base} \\times 10^{{{a_exp}}})\\cdot e^{{{b:.2f} \\cdot x}} + {c:.2f}$'

                color = cmap(j)  # Use colormap to determine the color

                axs[i].plot(rent_exp_data, fitted_values, label=label, color=color, linewidth=3, alpha=0.7)

            except RuntimeError:
                print(f"Error: Unable to fit exponential curve for column '{column}' in file '{filename}'")
                continue

        if fitted_values_region:
            shortest_length = min(len(values) for values in fitted_values_region)
            print(f"shot length: {shortest_length}")
            if rent_length is not None and rent_length <= shortest_length:
                shortest_length = rent_length
        else:
            print("Not enough data points were successfully fitted to compare lengths.")
            shortest_length = None
        resized_fitted_values = []
        for values in fitted_values_region:
            resized_values = values[:shortest_length]  # Keep only the first 'shortest_length' elements
            resized_fitted_values.append(resized_values)
        print(resized_fitted_values)
        for k in range(len(resized_fitted_values) - 1):
            axs[i].fill_between(max(rent_exp, key=len)[:shortest_length], resized_fitted_values[k],
                                resized_fitted_values[k + 1],
                                color=cmap(k), alpha=0.3)

        # Further plotting logic and setup as in your original code
        axs[i].set_xlabel('Rent Exponent')
        axs[i].set_ylabel('Value')
        axs[i].set_title(f'Exponential Fit for {column}')
        axs[i].legend()
        axs[i].grid(True)

    plt.tight_layout()
    directory = os.path.dirname(filenames[0])

    plt.savefig(os.path.join(directory, 'rent_exp_influence2vpr_flow.png'))
    plt.show()


def find_vpr_data_files(directory):
    """
    Search for all files ending with '_vpr_data.csv' in the specified directory and its subdirectories.
    """
    csv_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('_vpr_data.csv'):
                csv_files.append(os.path.join(root, file))
    return csv_files


def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else None


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python compvpr.py <folder> ")
        sys.exit(1)

    folder = sys.argv[1]
    csv_files = find_vpr_data_files(folder)

    if not csv_files:
        print("No '_vpr_data.csv' files found in the directory.")
        sys.exit(1)

    # Example function call, assuming this function is defined elsewhere
    draw_fit_in_diff_files(csv_files,
                           columns_to_fit=['time', 'cpd', 'total_wirelength', 'estimate_distance_1', 'estimate_distance_2',
                                           'packing_time', 'routing_time', 'placement_time'], rent_length=33)
    # draw_fit_in_diff_files(csv_files, columns_to_fit=['estimate_distance'], rent_length=33)
