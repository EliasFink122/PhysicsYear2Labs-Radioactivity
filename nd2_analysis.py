"""
Analyse nd^2 data.
"""
#############################################################################
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as op
import sys
#############################################################################

def main():
    # -- Import data --
    data = np.loadtxt(str(sys.argv[1]), skiprows=1, delimiter=',')
    cycle = int(sys.argv[2]) # time per cycle
    
    # -- Transpose data matrix --
    d = np.array([])
    n = np.array([])
    for meas in data:
        d = np.append(d, meas[0])
        n = np.append(n, meas[1])
    
    # -- Plot d-n --
    yerr_dn = np.sqrt(n*cycle) / cycle
    plt.plot(d, n, 'o')
    plt.errorbar(x=d, y=n, xerr=0.1, yerr=yerr_dn, fmt='none')
    plt.show()

    # -- Plot d-nd2 --
    nd2 = n * (d**2)
    yerr_dnd2 = yerr_dn * (d**2)
    plt.plot(d, nd2, 'o')
    plt.errorbar(x=d, y=nd2, xerr=0.1, yerr=yerr_dnd2, fmt='none')
    plt.show()



if __name__ == "__main__":
    main()