import json
import matplotlib.pyplot as plt
import math
import numpy as np
import matplotlib
from pylab import *

f = open('xyPoints1500.txt','r')

points = json.load(f)

x = []
y = []
for point in points:
    x.append(point[0])
    y.append(point[1]+5)

ftrack = open('track1500.txt', 'r')
trackPoints = json.load(ftrack)

xtrack = []
ytrack = []
for point in trackPoints:
    xtrack.append(point[0])
    ytrack.append(point[1])


# plt.pause(5)

origTheta = []
for i in range(1, len(x)):

    ydiff = (y[i] - y[i-1])
    xdiff = (x[i] - x[i-1])


    dir = math.atan2(ydiff,  xdiff)

    if i!= 1 and origTheta[-1] < 0 and dir > 2.5:
        dir -= 2*math.pi
    origTheta.append(dir)




origThetaDash = []
for i in range(1, len(origTheta)):

    ydiff = (origTheta[i] - origTheta[i-1])
    origThetaDash.append(ydiff)


dt  = x[0] - x[1]

def low_pass(x_new, y_old, cutoff = 0.007):
    
    alpha = 1 / (1 + 1 / (2 * dt* np.pi * cutoff))
    
    y_new = x_new * alpha + (1 - alpha) * y_old
    return y_new

def continuous_filter(xs):
    y_prev_low = 0  # initialization
    for x in xs:
        y_prev_low = low_pass(x, y_prev_low)
        yield y_prev_low


smoothThetaDash = np.array([out for out in continuous_filter(origThetaDash)])


smoothTheta = [smoothThetaDash[0]]


offset = smoothTheta[0] - origTheta[0]

offset -= 0.1
for i in range(1, len(smoothThetaDash)):
    smoothTheta.append(smoothTheta[-1] + smoothThetaDash[i])

smoothTheta.append(smoothTheta[-1])
smoothTheta.append(smoothTheta[-1])

for i in range(len(smoothTheta)):
    smoothTheta[i] -= offset




startSmooth = 20

for i in range(startSmooth+1):
    smoothTheta.pop(0)

smoothTheta =  smoothTheta + [smoothTheta[-1] for i in range(startSmooth+1)] 










projectedx = x.copy()
projectedy = [y[0]]

for i in range(1, len(smoothTheta)):
    dx = (projectedx[i]  - projectedx[i-1])
    dy = math.tan(smoothTheta[i])*dx
    if abs(dy) > 5:
        offset = -dy
    else: 
        offset = 0

    y1 = projectedy[-1] 
    yfinal =  y1 + dy + offset
    projectedy.append(yfinal)
    








plt.figure(4)
plt.plot(xtrack, ytrack,'+', label = 'track')
plt.legend()

plt.figure(3)
thismanager = get_current_fig_manager()
thismanager.window.wm_geometry("+2500+0")
plt.plot(x, y, label = 'Original')
plt.plot(projectedx, projectedy, label = 'Smoothened')
plt.plot(xtrack, ytrack,'+', label = 'track')
plt.legend()

plt.figure(1)
thismanager = get_current_fig_manager()
thismanager.window.wm_geometry("+1550+0")
plt.plot(origTheta, label = 'Original')
plt.plot(smoothTheta, label = 'Smoothened')
plt.legend()


plt.figure(2)
thismanager = get_current_fig_manager()
thismanager.window.wm_geometry("+1950+300")

plt.plot(origThetaDash, label = 'Original')
plt.plot(smoothThetaDash, label = 'Smoothened')
plt.legend()



plt.show()

