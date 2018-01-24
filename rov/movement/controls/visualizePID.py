import matplotlib.pyplot as plt
import numpy as np
from numpy import arange
from PID_Controller import PID


# This is Keith's scrap test file for PID Controllers
# If you've read past this line you've gone too far

setpoint = 5
maxTime = 10
dt = .01
x = 0  # Initial position

# Plot
fig, ax2 = plt.subplots()
ax2.set_title('PID Value')

pid = PID(5)
pid.p = 2
pid.i = 1
pid.d = .1

positions = np.array(arange(1,maxTime, dt))
counter = 0
for t in arange(1, maxTime, dt):
    e = setpoint - x
    u = pid.calculate(e, dt)

    # Plot position if controller controls velocity
    x += dt * u
    positions[counter]= x
    counter += 1

plt.plot(arange(1,maxTime,dt), positions)
plt.show()
plt.close()
