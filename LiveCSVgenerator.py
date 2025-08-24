# This code is written by Om Varma Dendukuri 
# ID NUMBER: 2025A4PS0677H

import csv
import time

#defining variables
AltitudeList = []
VelocityList = []

counter1 = 0

y_smooth_p = []
y_smooth_h = []
y_smooth_v = []

#reading csv Raw_Fight_Test_Data.py file
with open("Raw_Test_Flight_Data.csv", "r") as read_file:
    read_data = csv.reader(read_file)
    columns = next(read_data)

    # create or clear Real_Time.csv with the same headings
    with open("Real_Time.csv", "w", newline="") as write_file:
        write_data = csv.writer(write_file)
        write_data.writerow(columns)

    #iterates through rows

    for row in read_data:

        #to fix that random error (****** data)
        try:
            a = float(row[0])
        except:
            row[0] = previous_val

        #calculate altitude asing international standard atmosphere (ISA) model
        l = row[0]
        b = float(l)
        Altitude = 2 + (145366.45*(1-((b*0.01/1013.25) ** 0.190284)))
        row.pop(3)
        row.insert(3,str(Altitude))
        AltitudeList.append(Altitude)

        #velocity
        if counter1 == 0:
            Velocity = 0
            counter1 += 1
        else:
            Velocity = AltitudeList[-1] - AltitudeList[-2]
        row.pop(5)
        row.insert(5,str(Velocity))
        VelocityList.append(Velocity)

        #smoothening out graph using a low pass filter

        a = 0.2  #smoothing factor (0 < a < 1)

        #using the formula alpha*currentval + (1-alpha)*prevval

        #first case
        if row[1] == '1':
            y_smooth_p.append(float(row[0]))
            row.pop(2)
            row.insert(2,float(row[0]))

            y_smooth_h.append(float(row[3]))
            row.pop(4)
            row.insert(4,float(row[3]))

            y_smooth_v.append(float(row[5]))
            row.pop(6)
            row.insert(6,float(row[5]))
        else: #later cases
            y_smooth_p.append(a * float(row[0]) + (1 - a) * y_smooth_p[-1])
            row.pop(2)
            row.insert(2,a * float(row[0]) + (1 - a) * y_smooth_p[-1])

            y_smooth_h.append(a * float(row[3]) + (1 - a) * y_smooth_h[-1])
            row.pop(4)
            row.insert(4,a * float(row[3]) + (1 - a) * y_smooth_h[-1])

            y_smooth_v.append(a * float(row[5]) + (1 - a) * y_smooth_v[-1])
            row.pop(6)
            row.insert(6,a* float(row[5]) + (1 - a) * y_smooth_v[-1])

        #update Real_Time.csv with the live data
        with open("Real_Time.csv", "a", newline="") as write_file:
            write_live_data = csv.writer(write_file)
            write_live_data.writerow(row)

        #progress indicator
        print(f"Time {row[1]} Data: {row}")
        previous_val = row[0]

        #update time
        time.sleep(1)
