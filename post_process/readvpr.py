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
import sys
import csv

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

    rent_exps = [d["rent_exp"] for d in data]
    cpds = [d["cpd"] for d in data]
    times = [d["time"] for d in data]
    total_wirelengths = [d["total_wirelength"] for d in data]

    fig, axs = plt.subplots(3, 1, figsize=(8, 12))

    axs[0].scatter(rent_exps, cpds)
    axs[0].set_title('Critical Path Delay vs. Rent Exponent')
    axs[0].set_xlabel('Rent Exponent')
    axs[0].set_ylabel('Critical Path Delay (ns)')

    axs[1].scatter(rent_exps, total_wirelengths)
    axs[1].set_title('Total Wire Length vs. Rent Exponent')
    axs[1].set_xlabel('Rent Exponent')
    axs[1].set_ylabel('Total Wire Length (units of 1 clb segments)')

    axs[2].scatter(rent_exps, times)
    axs[2].set_title('VPR Whole Flow Running Time vs. Rent Exponent')
    axs[2].set_xlabel('Rent Exponent')
    axs[2].set_ylabel('Time (seconds)')

    # csv_filename = os.path.join(output_figures_folder, 'vpr_data.csv')
    # save_to_csv(data, csv_filename)

    plt.tight_layout()
    plt.savefig(os.path.join(output_figures_folder, 'rent_exp_influence2vpr_flow.png'))
    plt.show()
