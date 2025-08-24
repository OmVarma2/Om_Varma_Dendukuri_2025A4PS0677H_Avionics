# This code is written by Om Varma Dendukuri 
# ID NUMBER: 2025A4PS0677H

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.gridspec as gridspec
from scipy.ndimage import gaussian_filter1d
import numpy as np

#defining variables
AltitudeList = []
VelocityList = []
PressureList = []

AltitudeNoisey = []
VelocityNoisey = []
PressureNoisey = []

#Define colors of the all the graphs
plt.rcParams['font.family'] = 'Lucida Sans Unicode'     
plt.rcParams['font.size'] = 14            
plt.rcParams['axes.labelcolor'] = 'black'   
plt.rcParams['xtick.color'] = 'black'     
plt.rcParams['ytick.color'] = 'black'     
plt.rcParams['legend.labelcolor'] = 'black'  
plt.rcParams['legend.fontsize'] = 9

#color of background
fig = plt.figure(figsize=(10, 8), facecolor="lightgrey")
gs = gridspec.GridSpec(2, 2, figure=fig)

#position of the three graphs 
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, :])

#main title
fig.suptitle("REAL TIME FLIGHT DATA", fontsize=16, fontweight="bold")

#animaiton function
def animate(i):

    #read data
    data = pd.read_csv('Real_Time.csv')

    #extract data
    Time_x = data['Time'].values

    Pressure_Data_y = data['Pressure (Pa)'].values
    SPressure_Data_y = data['SPressure'].values
    PressureList.append(Pressure_Data_y)

    Velocity_Data_y = data['Velocity'].values
    SVelocity_Data_y = data['SVelocity'].values
    VelocityList.append(Velocity_Data_y)

    Altitude_Data_y = data['Altitude'].values
    SAltitude_Data_y = data['SAltitude'].values
    AltitudeList.append(Altitude_Data_y)

    #clearing axis
    ax1.cla()
    ax2.cla()
    ax3.cla()

    #Gaussian Smoothening
    SinVals = np.sin(Time_x * 0.1)

    PressureNoisy = Pressure_Data_y + SinVals
    VelocityNoisy = Velocity_Data_y + SinVals
    AltitudeNoisy = Altitude_Data_y + SinVals

    # Gaussian smoothing (same length as Time_x)
    y_gauss_p = gaussian_filter1d(PressureNoisy, sigma=2)
    y_gauss_v = gaussian_filter1d(VelocityNoisy, sigma=2)
    y_gauss_h = gaussian_filter1d(AltitudeNoisy, sigma=2)

    #pressure graphing
    ax1.plot(Time_x, SPressure_Data_y, label='Noise Reduced Pressure')
    ax1.plot(Time_x, Pressure_Data_y, label='Pressure', marker='o')
    ax1.plot(Time_x, y_gauss_p, label='Gaussian Smooth Pressure')
    ax1.legend(loc='upper left')
    ax1.set_title('Pressure vs Time LIVE')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Pressure (Pa)')

    #velocity graphing
    ax2.plot(Time_x, SVelocity_Data_y, label='Noise Reduced Velocity')
    ax2.plot(Time_x, Velocity_Data_y, label='Velocity',marker='o')
    ax2.plot(Time_x, y_gauss_v, label='Gaussian Smooth Velocity')
    ax2.legend(loc='upper left')
    ax2.set_title('Velocity vs Time LIVE')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Velocity (m/s)')

    #altitude graphing
    ax3.plot(Time_x, SAltitude_Data_y, label='Noise Reduced Altitude')
    ax3.plot(Time_x, Altitude_Data_y, label='Altitude',marker='o')
    ax3.plot(Time_x, y_gauss_h, label='Gaussian Smooth Altitude')
    ax3.legend(loc='upper left')
    ax3.set_title('Altitude vs Time LIVE')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Altitude (m)')
 
    #layout + space
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)

    #grid
    ax1.grid(True, linestyle="--", linewidth=0.7, color="gray")
    ax2.grid(True, linestyle="--", linewidth=0.7, color="gray")
    ax3.grid(True, linestyle="--", linewidth=0.7, color="gray")

#plot style + plot display
plt.style.use("ggplot")
ani = FuncAnimation(fig, animate, interval=1000)
plt.tight_layout()
plt.show()