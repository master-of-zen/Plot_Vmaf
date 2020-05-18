#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt


filename = sys.argv[1]

def read_vmaf_xml(file):
        with open(file, 'r') as f:
            file = f.readlines()
            file = [x.strip() for x in file if 'vmaf="' in x]
            vmafs = []
            for i in file:
                vmf = i[i.rfind('="') + 2: i.rfind('"')]
                vmafs.append(float(vmf))

            vmafs = [round(float(x), 3) for x in vmafs if type(x) == float]

        # Data
        x = [x for x in range(len(vmafs))]
        mean = round(sum(vmafs) / len(vmafs), 3)
        perc_1 = round(np.percentile(vmafs, 1), 3)
        perc_25 = round(np.percentile(vmafs, 25), 3)
        perc_75 = round(np.percentile(vmafs, 75), 3)

        # Plot
        plt.figure(figsize=(15, 4))
        [plt.axhline(i, color='grey', linewidth=0.4) for i in range(0, 100)]
        [plt.axhline(i, color='black', linewidth=0.6) for i in range(0, 100, 5)]
        plt.plot(x, vmafs, label=f'Frames: {len(vmafs)}\nMean:{mean}'
                                 f'\n1%: {perc_1} \n25%: {perc_25} \n75%: {perc_75}', linewidth=0.7)
        plt.ylabel('VMAF')
        plt.legend(loc="lower right")
        plt.ylim(int(perc_1), 100)
        plt.tight_layout()
        plt.margins(0)

        # Save
        file_name = 'plot.png'
        plt.savefig(file_name, dpi=500)

read_vmaf_xml(filename)

