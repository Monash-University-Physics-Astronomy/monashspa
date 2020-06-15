# Playpen
# Scott Findlay
# 12th August 2019

import numpy as np
import matplotlib.pyplot as plt
import monashspa.PHS2061 as spa
from lmfit import fit_report

data = [
        #voltage[V], u(voltage)[V], current[A], u(current)[A]
        [1.0, 1.0, 0.8],
        [2.0, 3.0, 0.8],
        [3.0, 7.0, 0.8],
        [4.0, 8.0, 0.8],
                ]
data = np.array(data)

xvals = data[:,0]
yvals = data[:,1]
u_yvals = data[:,2]

fit_results = spa.linear_fit(xvals,yvals, u_y=u_yvals)
y_fit = fit_results.best_fit
u_y_fit = fit_results.eval_uncertainty(sigma=1)

fit_parameters = spa.get_fit_parameters(fit_results)
print(fit_parameters)

plt.figure(1)
plt.errorbar(xvals, yvals, yerr=u_yvals, marker="o", linestyle="None", color="black",label="experimental data")
plt.plot(xvals, y_fit, marker="None", linestyle="-", color="black",label="linear fit")
plt.fill_between(xvals,y_fit-u_y_fit,y_fit+u_y_fit, color="lightgrey",label="uncertainty in linear fit")
plt.xlabel("X")
plt.ylabel("Y")
leg = plt.legend(bbox_to_anchor=(1,1))
#plt.savefig('figure00.png',dpi=600, bbox_extra_artists=(leg,), bbox_inches='tight')
plt.show()


buff = []
add = buff.append
add("[[Fit Statistics]]")
add("    # data points      = %s" % (fit_results.ndata))
add("    # variables        = %s" % (fit_results.nvarys))
add("    chi-square         = %s" % (fit_results.chisqr))
add("    reduced chi-square = %s" % (fit_results.redchi))
print('\n'.join(buff))

#------------------------
# Quadratic fit
#------------------------

nonlinear_model = spa.make_lmfit_model("A*x*x+B*x+C")
nonlinear_params = nonlinear_model.make_params(A=1,B=0,C=1)
fit_results_nl = spa.model_fit(nonlinear_model,nonlinear_params,xvals,yvals,u_y=u_yvals)
y_fit_nl = fit_results_nl.best_fit
u_y_fit_nl = fit_results_nl.eval_uncertainty(sigma=1)

fit_parameters_nl = spa.get_fit_parameters(fit_results_nl)
print('\n\n',fit_parameters_nl)

xwide = np.linspace(0, 5, 100)
ywide = fit_results_nl.eval(x=xwide)
u_ywide = fit_results_nl.eval_uncertainty(x=xwide,sigma=1)

plt.figure(2)
plt.title("Figure 2: Quadratic fit to input data")
plt.errorbar(xvals, yvals, yerr=u_yvals, marker="o", linestyle="None", color="black",label="experimental data")
plt.plot(xwide, ywide, marker="None", linestyle="-", color="black",label="quadratic fit")
plt.fill_between(xwide,ywide-u_ywide,ywide+u_ywide, color="lightgrey",label="uncertainty in fit")
plt.xlabel("X")
plt.ylabel("Y")
leg = plt.legend(bbox_to_anchor=(1,1))
plt.show()

buff = []
add = buff.append
add("[[Fit Statistics]]")
add("    # data points      = %s" % (fit_results_nl.ndata))
add("    # variables        = %s" % (fit_results_nl.nvarys))
add("    chi-square         = %s" % (fit_results_nl.chisqr))
add("    reduced chi-square = %s" % (fit_results_nl.redchi))
print('\n'.join(buff))

#------------------------
# Cubic fit
#------------------------

nonlinear_model = spa.make_lmfit_model("a*x*x*x+b*x*x+c*x+d")
nonlinear_params = nonlinear_model.make_params(a=1,b=0,c=0,d=1)
fit_results_nl = spa.model_fit(nonlinear_model,nonlinear_params,xvals,yvals,u_y=u_yvals)
y_fit_nl = fit_results_nl.best_fit
u_y_fit_nl = fit_results_nl.eval_uncertainty(sigma=1)

fit_parameters_nl = spa.get_fit_parameters(fit_results_nl)
print('\n\n',fit_parameters_nl)

xwide = np.linspace(0, 5, 100)
ywide = fit_results_nl.eval(x=xwide)
u_ywide = fit_results_nl.eval_uncertainty(x=xwide,sigma=1)

plt.figure(2)
plt.title("Figure 3: Cubic fit to input data")
plt.errorbar(xvals, yvals, yerr=u_yvals, marker="o", linestyle="None", color="black",label="experimental data")
plt.plot(xwide, ywide, marker="None", linestyle="-", color="black",label="cubic fit")
plt.fill_between(xwide,ywide-u_ywide,ywide+u_ywide, color="lightgrey",label="uncertainty in fit")
plt.xlabel("X")
plt.ylabel("Y")
leg = plt.legend(bbox_to_anchor=(1,1))
plt.show()

buff = []
add = buff.append
add("[[Fit Statistics]]")
add("    # data points      = %s" % (fit_results_nl.ndata))
add("    # variables        = %s" % (fit_results_nl.nvarys))
add("    chi-square         = %s" % (fit_results_nl.chisqr))
add("    reduced chi-square = %s" % (fit_results_nl.redchi))
print('\n'.join(buff))

#------------------------
# Constant fit
#------------------------

nonlinear_model = spa.make_lmfit_model("alpha + 0*x")
nonlinear_params = nonlinear_model.make_params(alpha=5)
fit_results_nl = spa.model_fit(nonlinear_model,nonlinear_params,xvals,yvals,u_y=u_yvals)
y_fit_nl = fit_results_nl.best_fit
u_y_fit_nl = fit_results_nl.eval_uncertainty(sigma=1)

fit_parameters_nl = spa.get_fit_parameters(fit_results_nl)
print('\n\n',fit_parameters_nl)

xwide = np.linspace(0, 5, 100)
ywide = fit_results_nl.eval(x=xwide)
u_ywide = fit_results_nl.eval_uncertainty(x=xwide,sigma=1)

plt.figure(2)
plt.title("Figure 4: Constant fit to input data")
plt.errorbar(xvals, yvals, yerr=u_yvals, marker="o", linestyle="None", color="black",label="experimental data")
plt.plot(xwide, ywide, marker="None", linestyle="-", color="black",label="constant fit")
plt.fill_between(xwide,ywide-u_ywide,ywide+u_ywide, color="lightgrey",label="uncertainty in fit")
plt.xlabel("X")
plt.ylabel("Y")
leg = plt.legend(bbox_to_anchor=(1,1))
plt.show()

buff = []
add = buff.append
add("[[Fit Statistics]]")
add("    # data points      = %s" % (fit_results_nl.ndata))
add("    # variables        = %s" % (fit_results_nl.nvarys))
add("    chi-square         = %s" % (fit_results_nl.chisqr))
add("    reduced chi-square = %s" % (fit_results_nl.redchi))
print('\n'.join(buff))
