#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 4/8/24 
# @Author  : Xiaoke Wang
# @Group   : UGent HES
# @File    : rent_norm2viz.py
# @Software: PyCharm, Ghent

import os
import pickle
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import sys
# from sklearn.linear_model import LinearRegression, RANSACRegressor
from statsmodels.nonparametric.kernel_regression import KernelReg
from sklearn import datasets, linear_model, kernel_ridge
from post-process.merge2csv import merge_2_csv

def rent_norm(t_dic, r):
    weighted_blocks = []
    for bl_dic in t_dic:
        w = 0
        for vertice in bl_dic:
            w += vertice*(bl_dic[vertice]**(1/r))
        weighted_blocks.append(w)
    return np.array(weighted_blocks)


def calculate_bin_means(rent_data_flat, blocks, n_bins):
    # Bin data
    max_blocks = blocks.max()
    bin_factor = max_blocks ** (1 / n_bins)
    bin_values = np.round(bin_factor ** np.arange(1, n_bins + 1))
    bin_values[-1] += 1  # Ensure covering max value

    # Mean and median per bin
    bin_means = []
    for i in range(n_bins):
        bin_mask = (blocks <= bin_values[i]) if i == 0 else ((blocks > bin_values[i - 1]) & (blocks <= bin_values[i]))
        bin_data = rent_data_flat[bin_mask]
        if bin_data.size > 0:
            blocks_mean = bin_data[:, 0].mean()
            pins_median = np.median(bin_data[:, 1])
            bin_means.append([blocks_mean, pins_median])

    bin_means = np.array(bin_means)
    return bin_means


def trend_line_ml(data):
    X = data[:, 0].reshape(-1, 1)
    y = data[:, 1]

    ransac = linear_model.RANSACRegressor(max_trials=30, min_samples=1000, residual_threshold=1.24, random_state=42)
    huber = linear_model.HuberRegressor(max_iter=1000, alpha=0.1, epsilon=4)

    model = huber
    model.fit(X, y)
    # inlier_mask = model.inlier_mask_
    # outlier_mask = np.logical_not(inlier_mask)
    outlier_mask = model.outliers_
    line_y_ransac = model.predict(X)
    coef = model.coef_[0]
    return line_y_ransac, coef, outlier_mask


def trend_line(data, slope_threshold=(0.2, 1)):
    filtered_data = []
    for i in range(1, len(data)):
        slope = (data[i, 1] - data[i - 1, 1]) / (data[i, 0] - data[i - 1, 0]) if (data[i, 0] - data[
            i - 1, 0]) != 0 else 0
        if slope_threshold[0] <= slope <= slope_threshold[1]:
            filtered_data.append(data[i - 1])
            filtered_data.append(data[i])

    if not filtered_data:
        return None, None, None, None

    # filtered data for tendline
    filtered_data = np.array(filtered_data)
    x, y = filtered_data[:, 0], filtered_data[:, 1]
    x_mean, y_mean = x.mean(), y.mean()
    x_err, y_err = x - x_mean, y - y_mean
    a = (x_err * y_err).sum() / (x_err ** 2).sum()
    b = y_mean - a * x_mean
    error = np.sum((y - (a * x + b)) ** 2) / len(filtered_data)

    return np.array([[x[0], a * x[0] + b], [x[-1], a * x[-1] + b]]), a, b, error


def visualize_rent(rent_path, output_filename='Rents_rule_real.png', output_figures_path="."):
    if not rent_path.endswith('.rent'):
        raise ValueError(f"Expected a .rent file, got {rent_path} instead.")
    with open(rent_path, "rb") as fp:  # Unpickling
        rent_data = pickle.load(fp)

    # Flatten data
    rent_data_flat = np.array([point for level in rent_data for point in level])
    blocks, pins = rent_data_flat[:, 0], rent_data_flat[:, 1]
    t_dic = rent_data_flat[:, 2]
    n_bins = len(rent_data)
    bin_means = calculate_bin_means(rent_data_flat[:,0:2], blocks, n_bins)
    # Trend line
    log_bin_means = np.log(bin_means)
    line, slope, _, _ = trend_line(log_bin_means)

    # use this slope for normalizing
    norm_blocks = rent_norm(t_dic, slope)
    prev_slope = slope
    for i in range(10):
        bin_means = calculate_bin_means(rent_data_flat[:,0:2], norm_blocks, n_bins)
        log_bin_means = np.log(bin_means)
        y_predict, slope, _ = trend_line_ml(np.stack((norm_blocks, pins), axis=1))
        if abs(prev_slope - slope) <= 0.0001:
            print(f"{i}: slope {slope} : prev_slope {prev_slope}")
            break

        prev_slope = slope
        norm_blocks = rent_norm(t_dic, slope)


    plt.figure(figsize=(10, 6))
    plt.scatter(norm_blocks, pins, alpha=0.1, label='Data Points')
    plt.scatter(bin_means[:, 0], bin_means[:, 1], s=100, color='red', alpha=0.85, edgecolors='w', linewidths=2,
                marker='o', label='Bin Means')
    plt.plot(norm_blocks, y_predict, color='red', label=f'Trend Line ML (Slope: {slope:.2f})')
    plt.xscale("log", base=2)
    plt.yscale("log", base=2)
    plt.xlabel('$B$ (Blocks)', size=15)
    plt.ylabel('$T$ (Terminals)', size=15)
    plt.plot(np.exp(line[:, 0]), np.exp(line[:, 1]), color='black', linewidth=2, linestyle='--',
             label=f'Slope (r) = {slope:.2f}')
    plt.title('Rent\'s Rule Visualization')
    plt.legend()

    os.makedirs(output_figures_folder, exist_ok=True)
    plt.savefig(os.path.join(output_figures_folder, output_filename))
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 rent2viz.py <rent_file_path>  <output_figures_folder>")
        sys.exit(1)

    rent_file_path = sys.argv[1]
    output_figures_folder = sys.argv[2]
    output_filename = rent_file_path + "_viz.png"

    visualize_rent(rent_file_path, output_filename, output_figures_folder)
    print(f"Visualization saved to {output_filename}")
