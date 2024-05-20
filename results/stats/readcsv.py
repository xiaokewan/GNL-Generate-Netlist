import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys


def plot_3d_comparison_data_vs_rent(csv_directory, output_directory, three_di=True):
    # y-axis: data, x-axis: rent exponent, color/z-axis: area
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]
    all_data = pd.DataFrame()
    markers = ['o', '^', 's', 'p', '*', '+', 'x', 'D', 'h', 'v']
    if len(csv_files) > len(markers):
        raise ValueError("More CSV files than defined markers. Please increase marker types.")

    for i, csv_file in enumerate(csv_files):
        df = pd.read_csv(os.path.join(csv_directory, csv_file))
        df['source_file'] = os.path.splitext(csv_file)[0]  # Add source file identifier
        df['marker'] = markers[i % len(markers)]  # Assign a marker
        all_data = pd.concat([all_data, df], ignore_index=True)

    exclusions = {'name', 'rent_exp', 'fpga_area', 'fpga_size', 'source_file', 'marker'}
    filtered_metrics = [col for col in all_data.columns if col not in exclusions]

    cols = 2
    rows = (len(filtered_metrics) + cols - 1) // cols

    fig = plt.figure(figsize=(15, rows * 4), dpi=600)

    for j, metric in enumerate(filtered_metrics, 1):
        ax = fig.add_subplot(rows, cols, j, projection='3d') if three_di is True else fig.add_subplot(rows, cols, j)
        # group data by source file for differentiated plotting
        grouped = all_data.groupby('source_file')
        for name, group in grouped:
            if three_di is True:
                scatter = ax.scatter(group['rent_exp'], group[metric], group['fpga_area'],
                                     c=group['fpga_area'], cmap='viridis', marker=group['marker'].iloc[0], label=name)
                if 'blocks' in group.columns and group['blocks'].notna().any():
                    for k in range(len(group)):
                        ax.text(group['rent_exp'].iloc[k], group[metric].iloc[k], group['fpga_area'].iloc[k],
                                f"{int(group['blocks'].iloc[k])}", color='red', fontsize='xx-small')
            else:
                scatter = ax.scatter(group['rent_exp'], group[metric], c=group['fpga_area'], cmap='viridis', marker=group['marker'].iloc[0], label=name)
                if 'blocks' in group.columns and group['blocks'].notna().any():
                    for k in range(len(group)):
                        ax.text(group['rent_exp'].iloc[k], group[metric].iloc[k],f"{int(group['blocks'].iloc[k])}", color='red', fontsize='xx-small')

        ax.set_xlabel('Rent Exponent')
        ax.set_zlabel('FPGA Area') if three_di is True else None
        ax.set_ylabel(metric)
        ax.set_title(f'Scatter Plot of {metric}')
        ax.legend(title='Source File')
        cbar = fig.colorbar(scatter, ax=ax, shrink=0.7)
        cbar.set_label(metric)

    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, 'combined_scatter_plots.png')) if three_di is False else plt.savefig(os.path.join(output_directory, 'combined_scatter_plots_3d.png'))
    plt.close()


def plot_3d_comparison_area_vs_rent(csv_directory, output_directory, three_di=True):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]
    all_data = pd.DataFrame()
    markers = ['o', '^', 's', 'p', '*', '+', 'x', 'D', 'h', 'v']
    if len(csv_files) > len(markers):
        raise ValueError("More CSV files than defined markers. Please increase marker types.")

    for i, csv_file in enumerate(csv_files):
        df = pd.read_csv(os.path.join(csv_directory, csv_file))
        df['source_file'] = os.path.splitext(csv_file)[0]  # Add source file identifier
        df['marker'] = markers[i % len(markers)]  # Assign a marker
        all_data = pd.concat([all_data, df], ignore_index=True)

    exclusions = {'name', 'rent_exp', 'fpga_area', 'fpga_size', 'source_file', 'marker'}
    filtered_metrics = [col for col in all_data.columns if col not in exclusions]

    cols = 2
    rows = (len(filtered_metrics) + cols - 1) // cols

    fig = plt.figure(figsize=(15, rows * 4), dpi=600)

    for j, metric in enumerate(filtered_metrics, 1):
        ax = fig.add_subplot(rows, cols, j, projection='3d') if three_di is True else fig.add_subplot(rows, cols, j)
        # group data by source file for differentiated plotting
        grouped = all_data.groupby('source_file')
        for name, group in grouped:
            if three_di is True:
                scatter = ax.scatter(group['rent_exp'], group['fpga_area'], group[metric],
                                     c=group[metric], cmap='viridis', marker=group['marker'].iloc[0], label=name)
                if 'blocks' in group.columns and group['blocks'].notna().any():
                    for k in range(len(group)):
                        ax.text(group['rent_exp'].iloc[k], group['fpga_area'].iloc[k], group[metric].iloc[k],
                                f"{int(group['blocks'].iloc[k])}", color='red', fontsize='xx-small')
            else:
                scatter = ax.scatter(group['rent_exp'], group['fpga_area'], c=group[metric], cmap='viridis', marker=group['marker'].iloc[0], label=name)
                if 'blocks' in group.columns and group['blocks'].notna().any():
                    for k in range(len(group)):
                        ax.text(group['rent_exp'].iloc[k], group['fpga_area'].iloc[k],f"{int(group['blocks'].iloc[k])}", color='red', fontsize='xx-small')

        ax.set_xlabel('Rent Exponent')
        ax.set_ylabel('FPGA Area')
        ax.set_zlabel(metric) if three_di is True else None
        ax.set_title(f'Scatter Plot of {metric}')
        ax.legend(title='Source File')
        cbar = fig.colorbar(scatter, ax=ax, shrink=0.6)
        cbar.set_label(metric)

    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, 'combined_scatter_plots.png')) if three_di is False else plt.savefig(os.path.join(output_directory, 'combined_scatter_plots_3d.png'))
    plt.close()


def plot_3d_scatter_sperate(csv_directory, output_directory):
    # plot the csv data separately
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)


    csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]
    cmap = plt.colormaps.get_cmap('Set1')

    for i, csv_file in enumerate(csv_files):
        df = pd.read_csv(os.path.join(csv_directory, csv_file))

        metrics = df.T.index
        exclusions = {'name', 'rent_exp', 'fpga_area', 'fpga_size'}
        filtered_metrics = [metric for metric in metrics if metric not in exclusions]
        cols = 2
        rows = (len(filtered_metrics) + cols - 1) // cols  
        fig = plt.figure(figsize=(15, rows * 4), dpi=600)
        for j, metric in enumerate(filtered_metrics, 1):
            ax = fig.add_subplot(rows, cols, j, projection='3d')

            scatter = ax.scatter(df['rent_exp'], df['fpga_area'], df[metric], c=df[metric], cmap='viridis', marker='o')
            ax.set_xlabel('Rent Exponent')
            ax.set_ylabel('FPGA Area')
            ax.set_zlabel(metric)
            ax.set_title(f'Scatter Plot of {metric}')
            cbar = fig.colorbar(scatter, ax=ax, shrink=0.6)
            cbar.set_label(metric)

        plt.tight_layout()
        plt.savefig(os.path.join(output_directory, f'{os.path.splitext(csv_file)[0]}_scatter_plots.png'))
        plt.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python readvpr.py <log_folder> <output_figures_folder>")
        sys.exit(1)
    # Example usage of the function
    csv_folder = sys.argv[1]
    output_figures_dir = sys.argv[2]
    # plot_3d_scatter_sperate(csv_folder, output_figures_dir)
    plot_3d_comparison_data_vs_rent(csv_folder, output_figures_dir, three_di=True)