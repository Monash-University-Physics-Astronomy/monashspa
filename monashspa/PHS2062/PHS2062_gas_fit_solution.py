# Playpen
# Scott Findlay
# 12th August 2019

import os
import sys

import pandas

import numpy as np
import matplotlib.pyplot as plt

from lmfit import fit_report
from scipy import stats
from monashspa.common.fitting import linear_fit, get_fit_parameters, make_lmfit_model, model_fit
from monashspa.common.figures import savefig

# Read the data from file
data = None
try:
    fname = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'PHS2062_gas_data.csv')
    data = pandas.read_csv(fname, usecols=[0,1,2]).to_numpy()
except FileNotFoundError:
    print("ERROR: Failed to read CSV file with data. It should be in the same folder as the Python file.")
if type(data)=="NoneType":
    sys.exit(1)

volume = data[:,0]
u_volume = data[:,1]
temp = data[:,2]

# Fit the data to the ideal gas law
# Assume n=0.040, p=1.013
#
# V = nR/p * T = 0.03949 * R * T (fit for R/100 to get value close to 1)
#
ideal_gas_model = make_lmfit_model("0.03949*R*x")
ideal_gas_params = ideal_gas_model.make_params(R=0.01)
ideal_gas_fit_results = model_fit(ideal_gas_model, ideal_gas_params, temp, volume, u_y=u_volume)

ideal_gas_fit = ideal_gas_fit_results.best_fit
u_ideal_gas_fit = ideal_gas_fit_results.eval_uncertainty(sigma=1)
ideal_gas_fit_parameters = get_fit_parameters(ideal_gas_fit_results)
pvalue = 1.0 - stats.chi2.cdf(ideal_gas_fit_results.chisqr,
                              ideal_gas_fit_results.ndata-ideal_gas_fit_results.nvarys)

print("""
[[Ideal gas law]]
=================
  p-value       = {pvalue:.2E}
""".format(pars=ideal_gas_fit_parameters, f=ideal_gas_fit_results, pvalue=pvalue))
print(ideal_gas_fit_results.fit_report())

fig, (ax1, ax2) = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios': [3, 1]})
ax1.errorbar(temp, volume, yerr=u_volume, marker="", linestyle="None", color="black",label="experimental data")
ax1.plot(temp, ideal_gas_fit, marker="None", linestyle="-", color="black",label="linear fit")
ax1.fill_between(temp, ideal_gas_fit-u_ideal_gas_fit,ideal_gas_fit+u_ideal_gas_fit,
                 color="lightgrey",label="uncertainty in linear fit")
ax1.legend(bbox_to_anchor=(0.5,1))
ax1.set(ylabel="Volume (L)")
pull = (volume-ideal_gas_fit)/u_volume
ax2.plot(temp, pull, marker="*", linestyle="None", color="black")
ax2.plot([np.min(temp), np.max(temp)], [0,0], marker="None", linestyle="-", color="grey")
ax2.plot([np.min(temp), np.max(temp)], [1,1], marker="None", linestyle="dashed", color="grey")
ax2.plot([np.min(temp), np.max(temp)], [-1,-1], marker="None", linestyle="dashed", color="grey")
ax2.set(xlabel="Temperature (K)", ylabel="Pull")
scale = 1.1*np.max(np.abs(pull))
ax2.set_ylim(-scale, scale)
fig.suptitle('Fit with ideal gas law')
savefig('ideal_gas.png')


# Fit the data to van der Waals law. The fit parameters are
#
# R: the ideal gas constant
# a: the parameter describing how atoms stick together
# b: the volume taken up by the molecules
#
# V = n R T / p ( 1 + b p/(RT) - a p/(RT)^2 )
#
vdW_gas_model = make_lmfit_model("0.040/1.013*R*x*(1.0 + 1.013*b/(R*x) - 1.013*a/(R*R*x*x))")
vdW_gas_params = vdW_gas_model.make_params(R=1.0, a=20.0, b=1.0)
vdW_gas_fit_results = model_fit(vdW_gas_model, vdW_gas_params, temp, volume, u_y=u_volume)

vdW_gas_fit = vdW_gas_fit_results.best_fit
u_vdW_gas_fit = vdW_gas_fit_results.eval_uncertainty(sigma=1)
vdW_gas_fit_parameters = get_fit_parameters(vdW_gas_fit_results)
pvalue = 1.0 - stats.chi2.cdf(vdW_gas_fit_results.chisqr,vdW_gas_fit_results.ndata-vdW_gas_fit_results.nvarys)

print("""

[[VdW gas law]]
===============
  p-value       = {pvalue:.2E}
""".format(pvalue=pvalue))
print(vdW_gas_fit_results.fit_report())

fig, (ax1, ax2) = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios': [3, 1]})
ax1.errorbar(temp, volume, yerr=u_volume, marker="", linestyle="None", color="black",label="experimental data")
ax1.plot(temp, vdW_gas_fit, marker="None", linestyle="-", color="black",label="linear fit")
ax1.fill_between(temp, vdW_gas_fit-u_vdW_gas_fit,vdW_gas_fit+u_vdW_gas_fit,
                 color="lightgrey",label="uncertainty in linear fit")
ax1.legend(bbox_to_anchor=(0.5,1))
ax1.set(ylabel="Volume (L)")

pull = (volume-vdW_gas_fit)/u_volume
ax2.plot([np.min(temp), np.max(temp)], [0,0], marker="None", linestyle="-", color="grey")
ax2.plot([np.min(temp), np.max(temp)], [1,1], marker="None", linestyle="dashed", color="grey")
ax2.plot([np.min(temp), np.max(temp)], [-1,-1], marker="None", linestyle="dashed", color="grey")
ax2.plot(temp, pull, marker="*", linestyle="None", color="black")
ax2.set(xlabel="Temperature (K)", ylabel="Pull")
scale = 1.1*np.max(np.abs(pull))
ax2.set_ylim(-scale, scale)
fig.suptitle('Fit with van der Waals law')
savefig('vdW_gas.png')
plt.show()
