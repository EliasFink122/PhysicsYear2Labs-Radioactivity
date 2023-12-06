"""
This version of the code was written by Elias Fink and Timothy Chew.

Analyse nd^2 data.
"""
#############################################################################
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as op
import sys
from scipy.integrate import quad
from scipy.stats import chi2
#############################################################################

def main():
    # -- Import data --
    data = np.loadtxt(str(sys.argv[1]), skiprows=1, delimiter=',')
    cycle = int(sys.argv[2]) # time per cycle
    
    # -- Transpose data matrix --
    d = np.array([])
    n = np.array([])
    for meas in data:
        d = np.append(d, meas[0]/100)
        n = np.append(n, meas[1])
    
    # -- Plot d-n --
    yerr_dn = np.sqrt(n*cycle) / cycle # errors from histogram
    if False:
        plt.plot(d, n, 'o')
        plt.errorbar(x=d, y=n, xerr=0.1, yerr=yerr_dn, fmt='none')
        plt.show()
    
    # -- Calculate nd2 and account for effects --
    nd2 = n * (d**2)

    att_fit, _ = op.curve_fit(exp, d[25:], nd2[25:], p0=[15, 2.6]) # attenuation
    print(att_fit, get_chisq(nd2[25:], exp(d[25:], *att_fit)))

    nps_fit, _ = op.curve_fit(lambda x, A: cs(x, A) + exp(x, *att_fit) - exp(0, *att_fit), d[:20], nd2[:20], p0=[5.5e5]) # non-point source
    print(nps_fit, get_chisq(nd2[1:10], cs(d[1:10], *nps_fit)))

    # -- Plot d-nd2 and fit --
    yerr_dnd2 = yerr_dn * (d**2) # errors from histogram scaled to nd^2
    d_fit = np.linspace(0, 1, 500)
    trans_nps = np.linspace(100, 100, 500)
    trans_att = np.linspace(0, 0, 500)
    plt.xlabel("$d \; [m]$")
    plt.ylabel("$nd^2 \; [m^2s^{-1}]$")
    plt.plot(d, nd2, 'o')
    plt.plot(d_fit, exp(d_fit, *att_fit), '-', color='green', label='Attenuation effect')
    plt.plot(d_fit, cs(d_fit, *nps_fit), '-',color='red', label='NPS effect')
    plt.plot(d_fit, cs(trans_nps, *nps_fit) - cs(d_fit, *nps_fit), '-', color='orange', label='Influence of NPS effect')
    plt.plot(d_fit, exp(trans_att, *att_fit) - exp(d_fit, *att_fit), '-', color='aqua', label='Influence of attenuation effect')
    plt.errorbar(x=d, y=nd2, xerr=0.001, yerr=yerr_dnd2, fmt='none', capsize=3)
    plt.legend()
    plt.show()

# -- Account for attenuation --
def exp(x, A, k):
    return A * np.exp(-x/k)

# -- Calculate chi-squared --
def get_chisq(o, e):
    if len(o) == len(e):
        chisq = 0
        for i in range(len(o)):
            chisq += (o[i] - e[i])**2/e[i]
    else:
        print('[', len(o),',', len(e),']')

    dof = len(o) - 1
    p = chi2.cdf(chisq, dof)
    
    return chisq, p

# -- Account for non-point source --
def cylindrical_source_integrand(p, r, a): # define geometry of cylindrical source
    #p - radial coordinate centred on the source
    #r - perpendicular distance from source to detector
    #a - side length of detector assuming square
    return (1/np.pi) * np.arctan(a/2 * r/(r**2 + p**2)) * 1/np.sqrt(1 + (2/a * (r**2 + p**2)/r)**2) * p * 2*np.pi

def cs(x, A): # predict count rate of source at distance x (A: activity)
    source_diameter = 0.1#0.010
    detector_length = 0.015
    #rho and width correspond to source_diameter and detector_length respectively
    return [A/(np.pi*source_diameter**2/4) * quad(cylindrical_source_integrand, 0, source_diameter/2, args=(i, detector_length))[0] for i in x] * x**2

if __name__ == "__main__":
    main()