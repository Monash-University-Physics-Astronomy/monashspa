# Copyright 2021 School of Physics & Astronomy, Monash University
#
# This file is part of monashspa.
#
# monashspa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# monashspa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with monashspa.  If not, see <http://www.gnu.org/licenses/>.
import random
import os
import csv
import math

import numpy as np
import matplotlib.pyplot as plt

from lmfit import fit_report
from scipy import stats
from monashspa.common.fitting import linear_fit, get_fit_parameters, make_lmfit_model, model_fit
from monashspa.common.figures import savefig

temp = np.arange(start=-20.0, stop=50.0, step = 10.0)

x = 17.0e-6*10000*temp+np.random.normal(0.0,2.0, len(temp))
u_x = np.full((len(temp)), 2.0)

x = x + np.random.normal(20.0, 5.0, 1)

fname = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'quiz_data.csv')
with open(fname, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
    writer.writerow( ['Length change (x)' , 'Uncertainty in length change (ux)', 'Temperature (K)'] )
    for a, b, c in zip(x, u_x, temp):
        writer.writerow(["{0:>7.3f}   ".format(a), "{0:>14.3f}        ".format(b), "{0:>8.1f}".format(c)])



name = "linear model"

# Create the model and run fit
model = make_lmfit_model("a*x + b")
params = model.make_params(a=1.0, b=0.0)
fit_results = model_fit(model, params, temp, x, u_y=u_x)

# Extract result and print nicely
fit = fit_results.best_fit
u_fit = fit_results.eval_uncertainty(sigma=1)
fit_parameters = get_fit_parameters(fit_results)
pvalue = 1.0 - stats.chi2.cdf(fit_results.chisqr,
                              fit_results.ndata-fit_results.nvarys)

print("""
[[{name}]]
=================
  p-value       = {pvalue:.2E}
""".format(name=name, pvalue=pvalue))
print(fit_results.fit_report())


# Create some plots
fig, ax = plt.subplots(1)
ax.errorbar(temp, x, yerr=u_x, marker="x", linestyle="None", color="black",label="experimental data")
ax.plot(temp, fit, marker="None", linestyle="-", color="black",label="fit to {name}".format(name=name))
ax.legend(bbox_to_anchor=(0.6,1))
ax.set(xlabel = "Temp", ylabel="x")
fig.suptitle('Fit with {name}'.format(name=name))
plt.show()
#savefig('chisquare_linear.png'.format(name=name))

