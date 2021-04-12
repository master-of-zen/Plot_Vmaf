#!/usr/bin/env python3

import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import json
from math import log10
from statistics import mean, harmonic_mean


def read_json(file):
    with open(file, "r") as f:
        fl = json.load(f)
        return fl


def plot_multi_metrics(scores, vmaf_file_names):
    i = 0
    ymin = 100
    for vmaf in scores:
        x = [x for x in range(len(vmaf))]
        plot_size = len(vmaf)
        hmean = round(harmonic_mean(vmaf), 2)
        amean = round(mean(vmaf), 2)
        perc_1 = round(np.percentile(sorted(vmaf), 1), 3)
        perc_25 = round(np.percentile(sorted(vmaf), 25), 3)
        perc_75 = round(np.percentile(sorted(vmaf), 75), 3)

        if ymin > perc_1:
            ymin = perc_1

        plt.plot(
            x,
            vmaf,
            label=f"File: {vmaf_file_names[i]}\n"
            f"Frames: {len(vmaf)} Mean:{amean} - Harmonic Mean:{hmean}\n"
            f"1%: {perc_1}  25%: {perc_25}  75%: {perc_75}",
            linewidth=0.7,
        )
        plt.plot([1, plot_size], [amean, amean], ":")
        plt.annotate(f"Mean: {amean}", xy=(0, amean))
        i = i + 1
    if ymin > 90:
        ymin = 90

    plt.ylabel("VMAF")
    plt.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.1),
        fancybox=True,
        shadow=True,
        fontsize="x-small",
    )
    plt.ylim(int(ymin), 100)
    plt.tight_layout()
    plt.margins(0)

    # Save
    plt.savefig(args.output, dpi=500)


def plot_metric(scores, metric):

    x = [x for x in range(len(scores))]

    mean = round(sum(scores) / len(scores), 3)

    plot_size = len(scores)

    # get percentiles
    perc_1 = round(np.percentile(scores, 1), 3)
    perc_25 = round(np.percentile(scores, 25), 3)
    perc_75 = round(np.percentile(scores, 75), 3)

    # Plot
    figure_width = 3 + round((4 * log10(plot_size)))

    plt.figure(figsize=(figure_width, 5))

    if metric == "SSIM":
        [plt.axhline(i / 100, color="grey", linewidth=0.4) for i in range(0, 100)]
        [plt.axhline(i / 100, color="black", linewidth=0.6) for i in range(0, 100, 5)]
    else:
        [plt.axhline(i, color="grey", linewidth=0.4) for i in range(0, 100)]
        [plt.axhline(i, color="black", linewidth=0.6) for i in range(0, 100, 5)]

    plt.plot(
        x,
        scores,
        label=f"Frames: {len(scores)} Mean:{mean}\n"
        f"1%: {perc_1}  25%: {perc_25}  75%: {perc_75}",
        linewidth=0.7,
    )

    plt.plot([1, plot_size], [perc_1, perc_1], "-", color="red")
    plt.annotate(f"1%: {perc_1}", xy=(0, perc_1), color="red")

    plt.plot([1, plot_size], [perc_25, perc_25], ":", color="orange")
    plt.annotate(f"25%: {perc_25}", xy=(0, perc_25), color="orange")

    plt.plot([1, plot_size], [perc_75, perc_75], ":", color="green")
    plt.annotate(f"75%: {perc_75}", xy=(0, perc_75), color="green")

    plt.plot([1, plot_size], [mean, mean], ":", color="black")
    plt.annotate(f"Mean: {mean}", xy=(0, mean), color="black")
    plt.title(metric)
    plt.ylabel(metric)
    plt.legend(
        loc="upper center", bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True
    )

    if metric == "VMAF":
        top_y = 100
    else:
        top_y = max(scores)

    if metric in ("VMAF", "PSNR"):
        bottom_y = int(perc_1)
    else:
        bottom_y = perc_1

    plt.ylim(bottom_y, top_y)
    plt.tight_layout()
    plt.margins(0)

    # Save
    plt.savefig(args.output, dpi=500)


def main():
    to_plot = []
    vmaf_file_names = []
    for metric in args.metrics:
        for f in args.vmaf_file:
            jsn = read_json(f)
            temp_scores = [x["metrics"][metric.lower()] for x in jsn["frames"]]
            to_plot.append(temp_scores)
            vmaf_file_names.append(f)

        if len(args.metrics) == 1:
            plot_metric(to_plot[0], metric)
        else:
            plot_multi_metrics(metric, vmaf_file_names)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Plot vmaf to graph")
    parser.add_argument("vmaf_file", type=str, nargs="+", help="Vmaf log file")
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        type=str,
        default="plot.png",
        help="Graph output filename (default plot.png)",
    )
    parser.add_argument(
        "-m",
        "--metrics",
        default=["VMAF"],
        help="what metrics to plot",
        type=str,
        nargs="+",
        choices=["VMAF", "PSNR", "SSIM"],
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    main()
