#######################################################################
# Fit the data to the ideal gas law
# Assume n=0.040, p=1.013
#
# V = nR/p * T = 0.040 / 1.013 * R * T

# Change the filename to read a different name
datafile = 'PHS2062_gas_short_data.csv'

# Change the model you fit here. "x" takes the role of temperature
model = "0.040/1.013*R*x"

# Name of the model that you fit
name = "Ideal gas law"

#######################################################################

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
    folder = os.path.dirname(os.path.realpath(__file__))
    fname = os.path.join(folder, datafile)
    data = pandas.read_csv(fname, usecols=[0,1,2]).to_numpy()
except FileNotFoundError:
    print("ERROR: Failed to read CSV file {file} with data. It should be in the same folder {folder} as the Python file".format(file=datafile, folder=folder))

if type(data)==type(None):
    sys.exit(1)

volume = data[:,0]
u_volume = data[:,1]
temp = data[:,2]

# Create the model and run fit
gas_model = make_lmfit_model(model)
gas_params = gas_model.make_params(R=0.01)
gas_fit_results = model_fit(gas_model, gas_params, temp, volume, u_y=u_volume)


# Extract result and print nicely
gas_fit = gas_fit_results.best_fit
u_gas_fit = gas_fit_results.eval_uncertainty(sigma=1)
gas_fit_parameters = get_fit_parameters(gas_fit_results)
pvalue = 1.0 - stats.chi2.cdf(gas_fit_results.chisqr,
                              gas_fit_results.ndata-gas_fit_results.nvarys)

print("""
[[{name}]]
=================
  p-value       = {pvalue:.2E}
""".format(name=name, pvalue=pvalue))
print(gas_fit_results.fit_report())


# Create some plots
fig, (ax1, ax2) = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios': [3, 1]})
ax1.errorbar(temp, volume, yerr=u_volume, marker="*", linestyle="None", color="black",label="experimental data")
ax1.plot(temp, gas_fit, marker="None", linestyle="-", color="black",label="linear fit")
ax1.fill_between(temp, gas_fit-u_gas_fit,gas_fit+u_gas_fit,
                 color="lightgrey",label="uncertainty in linear fit")
ax1.legend(bbox_to_anchor=(0.5,1))
ax1.set(ylabel="Volume (L)")
pull = (volume-gas_fit)/u_volume
ax2.plot(temp, pull, marker="*", linestyle="None", color="black")
ax2.plot([np.min(temp), np.max(temp)], [0,0], marker="None", linestyle="-", color="grey")
ax2.plot([np.min(temp), np.max(temp)], [1,1], marker="None", linestyle="dashed", color="grey")
ax2.plot([np.min(temp), np.max(temp)], [-1,-1], marker="None", linestyle="dashed", color="grey")
ax2.set(xlabel="Temperature (K)", ylabel="Pull")
scale = 1.1*np.max(np.abs(pull))
ax2.set_ylim(-scale, scale)
fig.suptitle('Fit with {name}'.format(name=name))
savefig('{name}.png'.format(name=name))

plt.show()
