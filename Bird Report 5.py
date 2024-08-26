# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 13:03:11 2024

@author: al72
"""

import csv
import matplotlib.pyplot as plt
import numpy as np

# function to add hour cells to each record for pivot table
def addhours(x):
    for k in range (0, 24):
        x.append(0)
        
    return x

# function to sum the calls for each species
def total(x):
    sum = 0
    for k in range (2, len(x)):
        sum += x[k]
    
    x.append(sum)
    
    return (x)

# function to return common name for sorting
def commonNameKey(rec):
    
    return rec[0]

# initialise variables   
data = []
# add report data
#####################
station = 'Birdweather PUC-4632'
location = 'Butterfactory Lane'
#location = 'North Haven, NSW'
#location = 'Wiangaree, NSW'
#location = 'Oberon, Wiangaree, North Haven'
#####################
#station = 'BirdNET-Pi 4325'
#location = 'Chatham Valley'
#####################
filename = "D:/Documents/Birdweather/4632 OBR WIA NH July 24.csv"
with open(filename, 'r') as file:
    csvreader = csv.reader(file)
    # read the header field names
    header = next(csvreader)
    # only keep the first 3
    header = header[0:3]
    # add field names for Date and Hour
    header.append('Date')
    header.append('Hour')
    # read the data row by row
    for row in csvreader:
        #only keep the first 3 fields
        row = row[0:3]
        data.append(row)

# calculate the date range
startdate = data[0][0][0:10]
enddate = data[len(data)-1][0][0:10]
daterange = startdate+' to '+enddate
        
# extract the date and hour and add to each record
for i in range (0, len(data)):
    line = data[i]  
    # get the date as a string          
    date = line[0][0:10]
    #get the hour as in integer
    hour = int(line[0][11:13])
    # add them to the record
    data[i].append(date)
    data[i].append(hour)

#make a header for the hour pivot table    
header1 = ['Common Name', 'Scientific Name']
for i in range (0,24):
    header1.append(i)

# make a grand total for the hour pivot table    
grandtotal = ['Grand','Total:']
addhours(grandtotal)

# create the pivot table
hourPivot = [['', '']]
addhours(hourPivot[0])
#print(hourPivot)

for i in range (0, len(data)):
    found = False
    # complete the first line of the pivot table with data
    if i == 0:
        # add the common name
        hourPivot[0][0] = data[i][1]
        # add the scientific name
        hourPivot[0][1] = data[i][2]
        # increment the hour of the call
        hourPivot[0][data[i][4]+2] += 1
        # increment the grand total
        grandtotal[data[i][4]+2] += 1
    else:
        # find the correct line of the pivot table
        for j in range (0, len(hourPivot)):
            if hourPivot[j][0] == data[i][1]:
                # increment the correct hour and grandtotal
                hourPivot[j][data[i][4]+2] += 1
                grandtotal[data[i][4]+2] += 1
                found = True
                break
        
        # add a new record if the species was not found
        if not found:
            # add common name
            hourPivot.append([data[i][1]])
            # add scientific name
            hourPivot[len(hourPivot)-1].append(data[i][2])
            # append hours cells
            addhours(hourPivot[len(hourPivot)-1])
            # increment the correct hour cell
            hourPivot[len(hourPivot)-1][data[i][4]+2] += 1
            # increment the grand total
            grandtotal[data[i][4]+2] += 1
 
# sum the calls for each species
for i in range (0, len(hourPivot)):
    total(hourPivot[i])
    
#sort by Common Name
hourPivot.sort(key = commonNameKey)

# a Total to the Header    
header1.append('Total')

# add a grandtotal total
total(grandtotal)

# save the pivot table as a CSV file
filename1 = filename[0:len(filename)-4] 
filename1 = filename1+'HourPivot.csv'
print(filename1)

with open(filename1, 'w+') as f:
    writer = csv.writer(f)
    writer.writerow(header1)
    writer.writerows(hourPivot)
    writer.writerow(grandtotal)
   
# plot hour pivot table
fig = plt.figure(figsize=(20,14), dpi=150)       # set to page size in inches
fig.suptitle('Time of Day Bird Calls', weight='black', color='b', size='x-large')
fig.text(0.5, 0.94, 'Oberon Citizen Science Network (OCSN)\nhttps://oberon-citizen.science/', ha = 'center')
fig.text(0.125, 0.93, 'Station: '+station)
fig.text(0.125, 0.91, 'Location: '+location)
fig.text(0.9, 0.94, 'Date Range: '+daterange, ha = 'right') 
ax = fig.add_subplot(1,1,1)
ax.set_xlim(0,1)
ax.set_ylim(0,1)
ax.axes.set_axis_off()

#set some colours for the pivot table
cmap = plt.get_cmap('Paired', lut=12)
COLORS = ['#%02x%02x%02x' % tuple(int(col * 255) for col in cmap(i)[:3]) for i in range(12)]
COLORS = COLORS[1:][::2][:-1] + COLORS[::2][:-1]

# calculate the text spacing
xpos = [0, 0.08, 0.18]
xspace = (0.99-xpos[2])/24
for i in range (2,24+2):
    xpos.append(xpos[i]+xspace)
    
yspace = 1/(len(hourPivot)+3)
ypos = [1]
for i in range (1, len(hourPivot)+2):
    ypos.append(ypos[i-1]-yspace)

# print the header
for i in range (0, len(header1)):
    if i < 2:
        ax.text(xpos[i], ypos[0], header1[i], color = 'b', weight = 'black', ha='left', va = 'center')
    else:
        ax.text(xpos[i], ypos[0], header1[i], color = 'b', weight = 'black', ha='center', va = 'center')

# print the pivot table        
for j in range (0,len(hourPivot)):
    for i in range (0, len(hourPivot[j])):
        if i < 2:
            ax.text(xpos[i], ypos[j+1], hourPivot[j][i], ha='left', va = 'center', size='xx-small')
            if i == 1:
                ax.plot(xpos[i]-xspace/4, ypos[j+1], marker = 'o', markersize = xspace*500, color = COLORS[j % len(COLORS)], alpha=0.8)
        else:
            ax.text(xpos[i], ypos[j+1], hourPivot[j][i], ha='center', va = 'center', size='small')
            a = hourPivot[j][i]
            b = hourPivot[j][len(hourPivot[j])-1]
            alpha=np.sqrt(float(a)*0.64/float(b))
            ax.plot(xpos[i], ypos[j+1], marker = 'o', markersize = xspace*500, color = COLORS[j % len(COLORS)], alpha=alpha, zorder=-1)

# print the grand total            
for i in range (0, len(grandtotal)):
    if i < 2:
        ax.text(xpos[i], ypos[len(hourPivot)+1], grandtotal[i], color = 'b', weight = 'black', ha='left', va = 'center')
    else:
        ax.text(xpos[i], ypos[len(hourPivot)+1], grandtotal[i], color = 'b', weight = 'black', ha='center', va = 'center')

#build the filename for the pivot table
filename2 = filename1[0:len(filename1)-4]
filename2 = filename2+'.png'

# print the filename on the pivot table for reference
fig.text(0.125, 0.125, filename2, size='x-small')     

# save the final pivot table as a PNG file
plt.savefig(filename2)

# show the final figure
plt.show()

# Day Pivot table
#start a header for the day pivot table
header2 = ['Common Name', 'Scientific Name']

# initialise day pivot table (copy from the hour pivot table)
dayPivot = [['', '']]
for i in range (0, len(hourPivot)):
    if i == 0:
        dayPivot[i][0] = hourPivot[i][0]
        dayPivot[i][1] = hourPivot[i][1]
    else:
        dayPivot.append([hourPivot[i][0]])
        dayPivot[i].append(hourPivot[i][1])

# Initialise Grand Total
grandtotal2 = ['Grand','Total:']

# fill out the pivot table
for i in range (0, len(data)):
    if data[i][3] != header2[len(header2)-1]:
        header2.append(data[i][3])
        grandtotal2.append(0)
        for j in range (0, len(dayPivot)):
            dayPivot[j].append(0)
            
    for j in range (0,len(dayPivot)):
        if data[i][1] == dayPivot[j][0]:
            dayPivot[j][len(dayPivot[j])-1] += 1
            grandtotal2[len(grandtotal2)-1] += 1
            break
    
# sum the calls for each species
for i in range (0, len(dayPivot)):
    total(dayPivot[i])

# add total to the header    
header2.append('Total')

# add total to the grand total
total(grandtotal2)

# build the filename for CSV file
filename3 = filename[0:len(filename)-4] 
filename3 = filename3+'DayPivot.csv'
print(filename3)

# save the pivot table as a CSV file
with open(filename3, 'w+') as f:
    writer = csv.writer(f)
    writer.writerow(header2)
    writer.writerows(dayPivot)
    writer.writerow(grandtotal2)

# plot day pivot table
fig1 = plt.figure(figsize=(20,14), dpi=150)       # set to page size in inches
fig1.suptitle('Daily Bird Calls', weight='black', color='b', size='x-large')
fig1.text(0.5, 0.94, 'Oberon Citizen Science Network (OCSN)\nhttps://oberon-citizen.science/', ha = 'center')
fig1.text(0.125, 0.93, 'Station: '+station)
fig1.text(0.125, 0.91, 'Location: '+location)
fig1.text(0.9, 0.94, 'Date Range: '+daterange, ha = 'right') 
ax1 = fig1.add_subplot(1,1,1)
ax1.set_xlim(0,1)
ax1.set_ylim(0,1)
ax1.axes.set_axis_off()

# calculate the text spacing
xpos = [0, 0.08, 0.18]
xspace = (0.99-xpos[2])/(len(header2)-2)
for i in range (2, len(header2)):
    xpos.append(xpos[i]+xspace)
    
yspace = 1/(len(dayPivot)+2)
#rad = min(xspace, yspace)
ypos = [1]
for i in range (1, len(dayPivot)+2):
    ypos.append(ypos[i-1]-yspace)

# print the header
for i in range (0, len(header2)):
    if i < 2:
        ax1.text(xpos[i], ypos[0], header2[i], color = 'b', weight = 'black', ha='left', va = 'center')
    else:
        ax1.text(xpos[i], ypos[0], header2[i], color = 'b', weight = 'black', rotation=60)

# print the pivot table        
for j in range (0,len(dayPivot)):
    for i in range (0, len(dayPivot[j])):
        if i < 2:
            ax1.text(xpos[i], ypos[j+1], dayPivot[j][i], ha='left', va = 'center', size='xx-small')
            if i == 1:
                ax1.plot(xpos[i]-0.01, ypos[j+1], marker = 'o', markersize = 20, color = COLORS[j % len(COLORS)], alpha=0.8)
        else:
            ax1.text(xpos[i], ypos[j+1], dayPivot[j][i], ha='center', va = 'center', size='small')
            a = dayPivot[j][i]
            b = dayPivot[j][len(dayPivot[j])-1]
            alpha=np.sqrt(float(a)*0.64/float(b))
            ax1.plot(xpos[i], ypos[j+1], marker = 'o', markersize = 20, color = COLORS[j % len(COLORS)], alpha=alpha, zorder=-1)

# print the grandtotal            
for i in range (0, len(grandtotal2)):
    if i < 2:
        ax1.text(xpos[i], ypos[len(dayPivot)+1], grandtotal2[i], color = 'b', weight = 'black', ha='left', va = 'center')
    else:
        ax1.text(xpos[i], ypos[len(dayPivot)+1], grandtotal2[i], color = 'b', weight = 'black', ha='center', va = 'center')

# build a filename for the pivot table
filename4 = filename3[0:len(filename3)-4]
filename4 = filename4+'.png'

# prin tthe filename on the pivit table for reference
fig1.text(0.125, 0.125, filename4, size='x-small')     

# save the final pivot table as a PNG file
plt.savefig(filename4)

# show the final figure
plt.show()
