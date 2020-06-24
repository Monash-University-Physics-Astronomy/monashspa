import random
import os
import csv
import math

import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import solve_ivp
from monashspa.common.figures import savefig


# Gas data created according to van der Waals law

a_vdW = 20*1.370 # 20 * Nitrogen
b_vdW = 50*0.0387 # 50 * Nitrogen

n_gas = 0.040 # moles
R_gas = 0.08314 # L bar K^-1 mol^-1

volume = np.arange(start=0.3, stop=2.0, step=0.05) # L
volume = volume + np.random.normal(0.0, 0.04, len(volume))
pressure = 1.013 # bar

temp_vdW = ( pressure*volume + a_vdW*n_gas*n_gas*(1-n_gas*b_vdW) - pressure*n_gas*b_vdW ) / (n_gas*R_gas)
temp_ideal = ( pressure*volume ) / (n_gas*R_gas)
volume_data = volume + np.random.normal(0.0, 0.01, len(volume))
u_volume_data = np.full((len(temp_vdW)), 0.01)

fname = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'PHS2062_gas_data.csv')
with open(fname, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
    writer.writerow( ['volume (L)', 'Volume uncertainty (L)', 'Temperature (K)'] )
    for v, u_v, t in zip(volume_data, u_volume_data, temp_vdW):
        writer.writerow(["{0:>7.3f}   ".format(v), "{0:>14.3f}        ".format(u_v), "{0:>8.1f}".format(t)])



volume = np.arange(start=1.0, stop=1.25, step=0.03) # L
volume = volume + np.random.normal(0.0, 0.015, len(volume))
pressure = 1.013 # bar

temp_vdW = ( pressure*volume + a_vdW*n_gas*n_gas*(1-n_gas*b_vdW) - pressure*n_gas*b_vdW ) / (n_gas*R_gas)
temp_ideal = ( pressure*volume ) / (n_gas*R_gas)
volume_data = volume + np.random.normal(0.0, 0.03, len(volume))
u_volume_data = np.full((len(temp_vdW)), 0.01)

fname = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'PHS2062_gas_short_data.csv')
with open(fname, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
    writer.writerow( ['volume (L)', 'Volume uncertainty (L)', 'Temperature (K)'] )
    for v, u_v, t in zip(volume_data, u_volume_data, temp_vdW):
        writer.writerow(["{0:>7.3f}   ".format(v), "{0:>14.3f}        ".format(u_v), "{0:>8.1f}".format(t)])


volume = np.arange(start=1.0, stop=1.25, step=0.02) # L
volume = volume + np.random.normal(0.0, 0.015, len(volume))
pressure = 1.013 # bar

temp_vdW = ( pressure*volume + a_vdW*n_gas*n_gas*(1-n_gas*b_vdW) - pressure*n_gas*b_vdW ) / (n_gas*R_gas)
temp_ideal = ( pressure*volume ) / (n_gas*R_gas)
volume_data = volume + np.random.normal(0.0, 0.03, len(volume))
u_volume_data = np.full((len(temp_vdW)), 0.03)

fname = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'PHS2062_gas_short_2_data.csv')
with open(fname, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
    writer.writerow( ['volume (L)', 'Volume uncertainty (L)', 'Temperature (K)'] )
    for v, u_v, t in zip(volume_data, u_volume_data, temp_vdW):
        writer.writerow(["{0:>7.3f}   ".format(v), "{0:>14.3f}        ".format(u_v), "{0:>8.1f}".format(t)])


        


# Measured period of large angle pendulum with friction

def pendulum(t, y):
    return [ y[1] , -9.82 /50. * math.sin(y[0]) - 0.025 * y[1] ]

def zerocrossing(t, y):
    return y[0]
zerocrossing.direction=1.0

sol = solve_ivp(pendulum, [0, 300], [math.pi/2., 0.0], events=zerocrossing, max_step=0.1)

# Assume that acuracy of timings are better when pendulum is moving fast
n_crossings = len(sol.t_events[0])
timeuncertainty = np.linspace(0.05, 0.3, n_crossings)
crossingtimes = sol.t_events[0] + np.random.normal(0.0, timeuncertainty)
periods = crossingtimes[1:-1] - crossingtimes[0:-2]
u_periods = math.sqrt(2)*timeuncertainty[:-2]
count = np.linspace(0,n_crossings-2,n_crossings-1)

fname = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'PHS2062_pendulum_data.csv')
with open(fname, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
    writer.writerow( ['Period (s) ', 'Period uncertainty ', '  count'] )
    for p, u_p, c in zip(periods, u_periods, count):
        writer.writerow(["{0:>8.3f}   ".format(p), "{0:>11.3f}        ".format(u_p), "{0:>5.1f}".format(c)])

plt.figure(1)
plt.plot(sol.t, sol.y[0], marker=None, linestyle="-", color="red",label="amplitude")
plt.xlabel("time (s)")
plt.ylabel("angle (rad)")
plt.title('pendulum')
savefig("pendulum_angle.png")
plt.show()
