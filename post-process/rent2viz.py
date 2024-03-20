#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 3/20/24 
# @Author  : Marieke Louage, Xiaoke Wang
# @Group   : UGent HES
# @File    : rent2viz.py.py
# @Software: PyCharm, Ghent
import os
import pickle
import matplotlib.pyplot as plt
import numpy as np


def trend_line(data):
    x, y = data[:, 0], data[:, 1]
    x_mean, y_mean = x.mean(), y.mean()
    x_err, y_err = x - x_mean, y - y_mean
    a = (x_err * y_err).sum() / (x_err ** 2).sum()
    b = y_mean - a * x_mean
    error = np.sum((y - (a * x + b)) ** 2) / len(data)
    return np.array([[x[0], a * x[0] + b], [x[-1], a * x[-1] + b]]), a, b, error


def visualize_rent(rent_path, output_filename='Rents_rule_real.png'):
    if not rent_path.endswith('.rent'):
        raise ValueError(f"Expected a .rent file, got {rent_path} instead.")
    with open(rent_path, "rb") as fp:  # Unpickling
        rent_data = pickle.load(fp)

    # Flatten data
    rent_data_flat = np.array([point for level in rent_data for point in level])
    blocks, pins = rent_data_flat[:, 0], rent_data_flat[:, 1]

    # Bin data
    n_bins = len(rent_data)
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

    # Trend line
    log_bin_means = np.log(bin_means)
    line, slope, _, _ = trend_line(log_bin_means)

    # Plotting
    plt.figure(figsize=(6, 8))
    plt.scatter(blocks, pins, alpha=0.1)
    plt.scatter(bin_means[:, 0], bin_means[:, 1], s=100, color='red')
    plt.xscale("log", base=2)
    plt.yscale("log", base=2)
    plt.xlabel('$B$', size=15)
    plt.ylabel('$T$', size=15)
    plt.plot(np.exp(line[:, 0]), np.exp(line[:, 1]), color='black', linewidth=2)
    plt.text(np.exp(line[0, 0]), np.exp(line[0, 1]), f'Slope (r) = {slope:.2f}', size=15)
    plt.savefig(output_filename)


if __name__ == '__main__':
    folder = "../rent_sweep/sweep"  # Adjust directory
    filenames = [f for f in os.listdir(folder) if f.endswith('.rent')]

    for filename in filenames:
        rent_path = os.path.join(folder, filename)
        output_filename = os.path.join(folder, f"{filename}_visualized.png")
        visualize_rent(rent_path, output_filename)
        print(f"Visualization saved to {output_filename}")