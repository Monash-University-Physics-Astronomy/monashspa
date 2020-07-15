import os
import sys

import numpy as np
import matplotlib.pyplot as plt

from lmfit import fit_report
from scipy import stats
from monashspa.common.fitting import linear_fit, get_fit_parameters, make_lmfit_model, model_fit
from monashspa.common.figures import savefig

xval = np.arange(start=-5.0, stop=5.0, step=0.8)
u_yval = 0.8 + xval*xval/15.
yval = 1.5*xval + np.random.normal(0.0,u_yval)

#######################################################################

# Name of the model that you fit
name = "linear model"

#######################################################################

# Create the model and run fit
model = make_lmfit_model("a*x + b")
params = model.make_params(a=1.0, b=0.0)
fit_results = model_fit(model, params, xval, yval, u_y=u_yval)

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
ax.errorbar(xval, yval, yerr=u_yval, marker="x", linestyle="None", color="black",label="experimental data")
ax.plot(xval, fit, marker="None", linestyle="-", color="black",label="fit to {name}".format(name=name))
#ax1.fill_between(xval, fit-u_fit,fit+u_fit,
#                 color="lightgrey",label="uncertainty in {name}".format(name=name))
ax.legend(bbox_to_anchor=(0.6,1))
ax.set(xlabel = "x", ylabel="y")
fig.suptitle('Fit with {name}'.format(name=name))
savefig('chisquare_linear.png'.format(name=name))


# Create some plots
fig, (ax1, ax2) = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios': [3, 1]})
ax1.errorbar(xval, yval, yerr=u_yval, marker="x", linestyle="None", color="black",label="experimental data")
ax1.plot(xval, fit, marker="None", linestyle="-", color="black",label="fit to {name}".format(name=name))
#ax1.fill_between(xval, fit-u_fit,fit+u_fit,
#                 color="lightgrey",label="uncertainty in {name}".format(name=name))
ax1.legend(bbox_to_anchor=(0.6,1))
ax1.set(ylabel="y")
pull = (yval-fit)/u_yval
ax2.plot(xval, pull, marker="*", linestyle="None", color="black")
ax2.plot([np.min(xval), np.max(xval)], [0,0], marker="None", linestyle="-", color="grey")
ax2.plot([np.min(xval), np.max(xval)], [1,1], marker="None", linestyle="dashed", color="grey")
ax2.plot([np.min(xval), np.max(xval)], [-1,-1], marker="None", linestyle="dashed", color="grey")
ax2.set(xlabel="x", ylabel="Pull")
scale = 1.1*np.max(np.abs(pull))
ax2.set_ylim(-scale, scale)
fig.suptitle('Fit with {name}'.format(name=name))
savefig('chisquare_linear_pull.png'.format(name=name))



#########################
# Wrong uncertainty scale
#########################

# Underestimate uncertainties in fit
# Create the model and run fit
yval = 1.5*xval + np.random.normal(0.0,u_yval)
model_underestimate = make_lmfit_model("a*x + b")
params_underestimate = model_underestimate.make_params(a=1.0, b=0.0)
fit_results_underestimate = model_fit(model_underestimate, params_underestimate, xval, yval, u_y=u_yval/3.0)


# Extract result and print nicely
fit_underestimate = fit_results_underestimate.best_fit
u_fit = fit_results_underestimate.eval_uncertainty(sigma=1)
fit_parameters = get_fit_parameters(fit_results_underestimate)
pvalue_underestimate = 1.0 - stats.chi2.cdf(fit_results_underestimate.chisqr,
                              fit_results_underestimate.ndata-fit_results_underestimate.nvarys)

print("""
[[{name}]]
=================
  p-value       = {pvalue:.2E}
""".format(name=name, pvalue=pvalue_underestimate))
print(fit_results_underestimate.fit_report())

# Create some plots
fig, (ax1, ax2) = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios': [3, 1]})
ax1.errorbar(xval, yval, yerr=u_yval/3.0, marker="x", linestyle="None", color="black",label="experimental data")
ax1.plot(xval, fit_underestimate, marker="None", linestyle="-", color="black",
         label="fit to {name}".format(name=name))
#ax1.fill_between(xval, fit-u_fit,fit+u_fit,
#                 color="lightgrey",label="uncertainty in {name}".format(name=name))
ax1.legend(bbox_to_anchor=(0.6,1))
ax1.set(ylabel="y")
pull = (yval-fit_underestimate)/(u_yval/3.0)
ax2.plot(xval, pull, marker="*", linestyle="None", color="black")
ax2.plot([np.min(xval), np.max(xval)], [0,0], marker="None", linestyle="-", color="grey")
ax2.plot([np.min(xval), np.max(xval)], [1,1], marker="None", linestyle="dashed", color="grey")
ax2.plot([np.min(xval), np.max(xval)], [-1,-1], marker="None", linestyle="dashed", color="grey")
ax2.set(xlabel="x", ylabel="Pull")
scale = 1.1*np.max(np.abs(pull))
ax2.set_ylim(-scale, scale)
fig.suptitle('Fit with {name}'.format(name=name))
savefig('chisquare_linear_underestimate.png'.format(name=name))


###############################
# Wrong model for uncertainties
###############################

# Underestimate uncertainties in fit
# Create the model and run fit
yval = 1.5*xval + np.random.normal(0.0,u_yval)
u_yval_wrong = (xval+6.0)/3.0
model_underestimate = make_lmfit_model("a*x + b")
params_underestimate = model_underestimate.make_params(a=1.0, b=0.0)
fit_results_underestimate = model_fit(model_underestimate, params_underestimate, xval, yval, u_y=u_yval_wrong)


# Extract result and print nicely
fit_underestimate = fit_results_underestimate.best_fit
u_fit = fit_results_underestimate.eval_uncertainty(sigma=1)
fit_parameters = get_fit_parameters(fit_results_underestimate)
pvalue_underestimate = 1.0 - stats.chi2.cdf(fit_results_underestimate.chisqr,
                              fit_results_underestimate.ndata-fit_results_underestimate.nvarys)

print("""
[[{name}]]
=================
  p-value       = {pvalue:.2E}
""".format(name=name, pvalue=pvalue_underestimate))
print(fit_results_underestimate.fit_report())

# Create some plots
fig, (ax1, ax2) = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios': [3, 1]})
ax1.errorbar(xval, yval, yerr=u_yval_wrong, marker="x", linestyle="None", color="black",label="experimental data")
ax1.plot(xval, fit_underestimate, marker="None", linestyle="-", color="black",
         label="fit to {name}".format(name=name))
#ax1.fill_between(xval, fit-u_fit,fit+u_fit,
#                 color="lightgrey",label="uncertainty in {name}".format(name=name))
ax1.legend(bbox_to_anchor=(0.6,1))
ax1.set(ylabel="y")
pull = (yval-fit_underestimate)/(u_yval_wrong)
ax2.plot(xval, pull, marker="*", linestyle="None", color="black")
ax2.plot([np.min(xval), np.max(xval)], [0,0], marker="None", linestyle="-", color="grey")
ax2.plot([np.min(xval), np.max(xval)], [1,1], marker="None", linestyle="dashed", color="grey")
ax2.plot([np.min(xval), np.max(xval)], [-1,-1], marker="None", linestyle="dashed", color="grey")
ax2.set(xlabel="x", ylabel="Pull")
scale = 1.1*np.max(np.abs(pull))
ax2.set_ylim(-scale, scale)
fig.suptitle('Fit with {name}'.format(name=name))
savefig('chisquare_linear_wrong_uncertainty.png'.format(name=name))

###############################
# Over fitting 
###############################
# 
# Create the model and run fit
yval = 1.5*xval + np.random.normal(0.0,u_yval)
model_underestimate = make_lmfit_model("a*x*x*x*x + b*x*x*x + c*x*x + d*x + e")
params_underestimate = model_underestimate.make_params(a=0.0, b=0.0, c=0.0, d=1.5, e=0.0)
fit_results_underestimate = model_fit(model_underestimate, params_underestimate, xval, yval, u_y=u_yval)


# Extract result and print nicely
fit_underestimate = fit_results_underestimate.best_fit
u_fit = fit_results_underestimate.eval_uncertainty(sigma=1)
fit_parameters = get_fit_parameters(fit_results_underestimate)
pvalue_underestimate = 1.0 - stats.chi2.cdf(fit_results_underestimate.chisqr,
                              fit_results_underestimate.ndata-fit_results_underestimate.nvarys)

print("""
[Quartic model]]
=================
  p-value       = {pvalue:.2E}
""".format(name=name, pvalue=pvalue_underestimate))
print(fit_results_underestimate.fit_report())

# Create some plots
fig, (ax1, ax2) = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios': [3, 1]})
ax1.errorbar(xval, yval, yerr=u_yval, marker="x", linestyle="None", color="black",label="experimental data")
ax1.plot(xval, fit_underestimate, marker="None", linestyle="-", color="black",
         label="fit to {name}".format(name=name))
#ax1.fill_between(xval, fit-u_fit,fit+u_fit,
#                 color="lightgrey",label="uncertainty in {name}".format(name=name))
ax1.legend(bbox_to_anchor=(0.6,1))
ax1.set(ylabel="y")
pull = (yval-fit_underestimate)/(u_yval)
ax2.plot(xval, pull, marker="*", linestyle="None", color="black")
ax2.plot([np.min(xval), np.max(xval)], [0,0], marker="None", linestyle="-", color="grey")
ax2.plot([np.min(xval), np.max(xval)], [1,1], marker="None", linestyle="dashed", color="grey")
ax2.plot([np.min(xval), np.max(xval)], [-1,-1], marker="None", linestyle="dashed", color="grey")
ax2.set(xlabel="x", ylabel="Pull")
scale = 1.1*np.max(np.abs(pull))
ax2.set_ylim(-scale, scale)
fig.suptitle('Fit with quartic function'.format(name=name))
savefig('chisquare_cubic.png'.format(name=name))




plt.show()
