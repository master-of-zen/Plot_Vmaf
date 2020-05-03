#!/usr/bin/env python3
import sys
from matplotlib import pyplot as plt


filename = sys.argv[1]

with open(filename,'r') as f:
    file = f.readlines()
    file = [x.strip() for x in file if 'vmaf="' in x]
    vmafs = []
    for i in file:
        vmf = i[i.rfind('="') + 2: i.rfind('"')]
        vmafs.append(float(vmf))

    vmafs = [round(float(x), 3) for x in vmafs if type(x) == float]
    plt.ylim((int(min(vmafs)), 100))
    d = min(vmafs)
    for i in range(int(d), 100, 1):
        plt.axhline(i, color='grey', linewidth=0.5)

x = [x for x in range(len(vmafs))]
plt.plot(x, vmafs)

# Save/close
plt.ylabel('VMAF')
plt.xlabel('Frames')
plt.title(f'{sys.argv[1]}, {len(vmafs)} ')
plt.tight_layout()
plt.savefig('fig', dpi=1000)
