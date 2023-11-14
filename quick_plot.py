"""
Plot histogram of DAQ output.
"""
#############################################################################
import numpy as np
import matplotlib.pyplot as plt
import sys
#############################################################################

def main():
    data = np.loadtxt(str(sys.argv[1])) # load data file

    plt.hist(data, int(sys.argv[2])) # create histogram
    plt.xlabel("Counts per cycle")
    plt.ylabel("Number of cycles")
    plt.title("Histogram of " + str(sys.argv[1]))
    plt.show()


if __name__ == "__main__":
    main()