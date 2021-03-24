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
import pandas
import os

import matplotlib.pyplot as plt

from lmfit import fit_report
from scipy import stats
from monashspa.common.fitting import linear_fit, get_fit_parameters, make_lmfit_model, model_fit
from monashspa.common.figures import savefig

try:
    __filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                              'quiz_data.csv')
    data = pandas.read_csv(__filepath).to_numpy()
except:
    data = "Warning: failed to import data from csv file. Possibly the monashspa library is not installed correctly."

x = data[:,0]
u_x = data[:,1]
temp = data[:,2]

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

aerr = fit_results.params['a'].stderr

print(f'The error on alpha is {aerr/10000:.2E}')

plt.show()
#savefig('chisquare_linear.png'.format(name=name))

