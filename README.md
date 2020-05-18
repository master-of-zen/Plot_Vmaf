# Plot_Vmaf
Simple script for vmaf plotting.  
![](plot.svg)

## Usage
```bash
python plot_vmaf.py [-h] [-o OUTPUT] vmaf_file
```

## Example
```bash
python plot_vmaf.py vmaf.xml -o plot.svg
```

## Options
```
Optional Arguments:
    -o/--output ["file"]    Graph output file, file extension will change type of output (default plot.png)
```

## Requirements
Python 3  
Matplotlib  
Numpy  
