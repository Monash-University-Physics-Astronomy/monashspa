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
    fname = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'PHS2062_pendulum_data.csv')
    data = pandas.read_csv(fname, usecols=[0,1,2]).to_numpy()
except FileNotFoundError:
    print("ERROR: Failed to read CSV file with data. It should be in the same folder as the Python file.")
if type(data)=="NoneType":
    sys.exit(1)

period = data[:,0]
u_period = data[:,1]
count = data[:,2]


fig, ax = plt.subplots(1)
ax.errorbar(count, period, yerr=u_period, marker="x", linestyle="None", color="black",label="experimental data")
ax.set(xlabel = 'count', ylabel="Period (s)")
fig.suptitle('Pendulum period')
savefig('pendulum_data.png')



# Let us assume that the period is constant

pendulum_model = make_lmfit_model("T", allow_constant_model=True)
pendulum_params = pendulum_model.make_params(T=2.0)
pendulum_fit_results = model_fit(pendulum_model, pendulum_params, count, period, u_y=u_period)

pendulum_fit = pendulum_fit_results.best_fit
u_pendulum_fit = pendulum_fit_results.eval_uncertainty(sigma=1)
pendulum_fit_parameters = get_fit_parameters(pendulum_fit_results)
pvalue = 1.0 - stats.chi2.cdf(pendulum_fit_results.chisqr,
                              pendulum_fit_results.ndata-pendulum_fit_results.nvarys)

print("""
[[Simple pendulum]]
===================
  p-value       = {pvalue:.2E}
""".format(pars=pendulum_fit_parameters, f=pendulum_fit_results, pvalue=pvalue))
print(pendulum_fit_results.fit_report())

pendulum_fit = np.full(len(count), pendulum_fit)
u_pendulum_fit = np.full(len(count), u_pendulum_fit[0])

fig, (ax1, ax2) = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios': [3, 1]})
ax1.errorbar(count, period, yerr=u_period, marker="x", linestyle="None", color="black",label="experimental data")
ax1.plot(count, pendulum_fit, marker="None", linestyle="-", color="black",label="linear fit")
ax1.fill_between(count, pendulum_fit-u_pendulum_fit,pendulum_fit+u_pendulum_fit,
                 color="lightgrey",label="uncertainty in linear fit")
ax1.legend(bbox_to_anchor=(0.5,1))
ax1.set(ylabel="Period (s)")
pull = (period-pendulum_fit)/u_period
ax2.plot(count, pull, marker="*", linestyle="None", color="black")
xrange = [np.min(count), np.max(count)]
ax2.plot(xrange, [0,0], marker="None", linestyle="-", color="grey")
ax2.plot(xrange, [1,1], marker="None", linestyle="dashed", color="grey")
ax2.plot(xrange, [-1,-1], marker="None", linestyle="dashed", color="grey")
ax2.set(xlabel="Count", ylabel="Pull")
scale = 1.1*np.max(np.abs(pull))
ax2.set_ylim(-scale, scale)
fig.suptitle('Fit to a constant period')
savefig('pendulum_constant_fit.png')



# Let us assume a linear change of period

pendulum_model = make_lmfit_model("T*(1.0+a*x)")
pendulum_params = pendulum_model.make_params(T=2.0, a=0)
pendulum_fit_results = model_fit(pendulum_model, pendulum_params, count, period, u_y=u_period)

pendulum_fit = pendulum_fit_results.best_fit
u_pendulum_fit = pendulum_fit_results.eval_uncertainty(sigma=1)
pendulum_fit_parameters = get_fit_parameters(pendulum_fit_results)
pvalue = 1.0 - stats.chi2.cdf(pendulum_fit_results.chisqr,
                              pendulum_fit_results.ndata-pendulum_fit_results.nvarys)

print("""
[[Linear change of period]]
===================
  p-value       = {pvalue:.2E}
""".format(pars=pendulum_fit_parameters, f=pendulum_fit_results, pvalue=pvalue))
print(pendulum_fit_results.fit_report())

fig, (ax1, ax2) = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios': [3, 1]})
ax1.errorbar(count, period, yerr=u_period, marker="x", linestyle="None", color="black",label="experimental data")
ax1.plot(count, pendulum_fit, marker="None", linestyle="-", color="black",label="linear fit")
ax1.fill_between(count, pendulum_fit-u_pendulum_fit,pendulum_fit+u_pendulum_fit,
                 color="lightgrey",label="uncertainty in linear fit")
ax1.legend(bbox_to_anchor=(0.5,1))
ax1.set(ylabel="Period (s)")
pull = (period-pendulum_fit)/u_period
ax2.plot(count, pull, marker="*", linestyle="None", color="black")
xrange = [np.min(count), np.max(count)]
ax2.plot(xrange, [0,0], marker="None", linestyle="-", color="grey")
ax2.plot(xrange, [1,1], marker="None", linestyle="dashed", color="grey")
ax2.plot(xrange, [-1,-1], marker="None", linestyle="dashed", color="grey")
ax2.set(xlabel="Count", ylabel="Pull")
scale = 1.1*np.max(np.abs(pull))
ax2.set_ylim(-scale, scale)
fig.suptitle('Fit with a linear term')
savefig('linear_pendulum.png')


# Let us assume an exponential change of period

pendulum_model = make_lmfit_model("T*(1.0+a*exp(-2*k*x))")
pendulum_params = pendulum_model.make_params(T=2.0, k=0)
pendulum_fit_results = model_fit(pendulum_model, pendulum_params, count, period, u_y=u_period)

pendulum_fit = pendulum_fit_results.best_fit
u_pendulum_fit = pendulum_fit_results.eval_uncertainty(sigma=1)
pendulum_fit_parameters = get_fit_parameters(pendulum_fit_results)
pvalue = 1.0 - stats.chi2.cdf(pendulum_fit_results.chisqr,
                              pendulum_fit_results.ndata-pendulum_fit_results.nvarys)

print("""
[[Exponential change of period]]
===================
  p-value       = {pvalue:.2E}
""".format(pars=pendulum_fit_parameters, f=pendulum_fit_results, pvalue=pvalue))
print(pendulum_fit_results.fit_report())

fig, (ax1, ax2) = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios': [3, 1]})
ax1.errorbar(count, period, yerr=u_period, marker="x", linestyle="None", color="black",label="experimental data")
ax1.plot(count, pendulum_fit, marker="None", linestyle="-", color="black",label="linear fit")
ax1.fill_between(count, pendulum_fit-u_pendulum_fit,pendulum_fit+u_pendulum_fit,
                 color="lightgrey",label="uncertainty in linear fit")
ax1.legend(bbox_to_anchor=(0.5,1))
ax1.set(ylabel="Period (s)")
pull = (period-pendulum_fit)/u_period
ax2.plot(count, pull, marker="*", linestyle="None", color="black")
xrange = [np.min(count), np.max(count)]
ax2.plot(xrange, [0,0], marker="None", linestyle="-", color="grey")
ax2.plot(xrange, [1,1], marker="None", linestyle="dashed", color="grey")
ax2.plot(xrange, [-1,-1], marker="None", linestyle="dashed", color="grey")
ax2.set(xlabel="Count", ylabel="Pull")
scale = 1.1*np.max(np.abs(pull))
ax2.set_ylim(-scale, scale)
fig.suptitle('Fit with an exponential term')
savefig('exponential_pendulum.png')




plt.show()
