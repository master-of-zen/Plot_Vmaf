#!/usr/bin/env python3

import sys, argparse
import numpy as np
import matplotlib.pyplot as plt

def plot_vmaf(vmafs):
    # Create datapoints
    x = [x for x in range(len(vmafs))]
    mean = round(sum(vmafs) / len(vmafs), 3)
    plot_size = len(vmafs)
    perc_1 = round(np.percentile(vmafs, 1), 3)
    perc_25 = round(np.percentile(vmafs, 25), 3)
    perc_75 = round(np.percentile(vmafs, 75), 3)

    # Plot
    figure_width = 3 + round((4 * log10(plot_size)))
    plt.figure(figsize=(figure_width, 5))
    [plt.axhline(i, color='grey', linewidth=0.4) for i in range(0, 100)]
    [plt.axhline(i, color='black', linewidth=0.6) for i in range(0, 100, 5)]
    plt.plot(x, vmafs, label=f'Frames: {len(vmafs)} Mean:{mean}\n'
                                f'1%: {perc_1}  25%: {perc_25}  75%: {perc_75}', linewidth=0.7)
    
    plt.plot([1, plot_size], [perc_1, perc_1], '-', color='red')
    plt.annotate(f'1%: {perc_1}', xy=(0, perc_1), color='red')

    plt.plot([1, plot_size], [perc_25, perc_25], ':', color='orange')
    plt.annotate(f'25%: {perc_25}', xy=(0, perc_25), color='orange')

    plt.plot([1, plot_size], [perc_75, perc_75], ':', color='green')
    plt.annotate(f'75%: {perc_75}', xy=(0, perc_75), color='green')

    plt.plot([1, plot_size], [mean, mean], ':', color='black')
    plt.annotate(f'Mean: {mean}', xy=(0, mean), color='black')
    plt.ylabel('VMAF')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True)
    plt.ylim(int(perc_1), 100)
    plt.tight_layout()
    plt.margins(0)

    # Save
    plt.savefig(args.output, dpi=500)

def read_vmaf_xml(file):
    with open(file, 'r') as f:
        file = f.readlines()
        file = [x.strip() for x in file if 'vmaf="' in x]
        vmafs = []
        for i in file:
            vmf = i[i.rfind('="') + 2: i.rfind('"')]
            vmafs.append(float(vmf))

        vmafs = [round(float(x), 3) for x in vmafs if type(x) == float]

    return(vmafs)

def main():
    vmafs = read_vmaf_xml(args.vmaf_file)
    plot_vmaf(vmafs)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Plot vmaf to graph')
    parser.add_argument('vmaf_file', type=str, help='Vmaf log file')
    parser.add_argument('-o','--output', dest='output', type=str, default='plot.png', help='Graph output filename (default plot.png)')
    
    return(parser.parse_args())

if __name__ == "__main__":
    args = parse_arguments()
    main()    
