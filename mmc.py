import argparse
parser = argparse.ArgumentParser()
# parser.parse_args()
parser.add_argument('--simT', type=int, default = 2000)
parser.add_argument('--arrR', type=int, default = 5) 
parser.add_argument('--serR', type=int, default = 3) 
parser.add_argument('--k', type=int, default = 2) 
args = parser.parse_args()

import random
import math 
import copy
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

arrivalList = []
serviceList = []
startList = []
departureList = []
serverList = [] 
# record the departure times of servers that are busy

# generate arrival time list (indepedent)
arrivalTime = 0
while arrivalTime < args.simT:
    arrivalTime += random.expovariate(args.arrR)
    arrivalList.append(arrivalTime)

'''
Show ArrivalList
'''
printArrivalList = [round(a, 3) for a in arrivalList]
# print(printArrivalList)
aList = copy.copy(arrivalList)

# run simulation
currentTime = 0
while currentTime < args.simT:

    currentTime = aList[0] # time stamp for reference

    if len(serverList) < args.k:
        startTime = aList[0]
    else: 
        startTime = serverList[serverList.index(min(serverList))]
        del(serverList[serverList.index(min(serverList))])
    
    startList.append(startTime)
    
    serviceTime = random.expovariate(args.serR)
    serviceList.append(serviceTime)

    departureTime = startTime + serviceTime

    departureList.append(departureTime)
    serverList.append(departureTime)
    aList.pop(0)

    if len(aList) == 0: break

    while len(serverList) > 0:
        if serverList[serverList.index(min(serverList))] < aList[0]:
            del(serverList[serverList.index(min(serverList))])
        else: break
    
'''
Performance Measure
'''
waitList = [startList[i] - arrivalList[i] for i in range(len(startList))]

# [1] plot waiting time 
# [2] plot service time 
bins = np.linspace(0, max(serviceList), 11)

plt.hist(waitList, bins ,facecolor='red', alpha=0.5,label='Waiting Time (Counts)')
arr=plt.hist(waitList, bins, facecolor='red', alpha=0.5)
for i in range(10):
    plt.text(arr[1][i], arr[0][i]+100, str(int(arr[0][i])),color='red')

plt.hist(serviceList, bins, facecolor='green', alpha=0.5,label='Service Time (Counts')
arr=plt.hist(serviceList, bins, facecolor='green', alpha=0.5)
for i in range(10):
    plt.text(arr[1][i], arr[0][i]+100, str(int(arr[0][i])),color='green')

plt.xlabel('Service Time')
plt.ylabel('Counts')
plt.title('Counts of Waiting & Service Time for {} Patients in {} Minutes'.format(len(waitList), args.simT))
plt.axis([min(serviceList), max(serviceList),0,len(serviceList)])
plt.grid(True)
plt.legend(loc='upper right')
plt.show()

avgWait = sum(waitList)/len(waitList)
avgService = sum(serviceList)/len(serviceList)
avgTime = avgWait + avgService
avgCustomer_inSys = avgTime * args.arrR

rho = args.arrR / (args.k * args.serR)
'''
Verify the True/Expected Waiting Time
'''
p1 = 0 
for n in range(args.k):
    p1 += (args.k*rho)**n / math.factorial(n)
p2 = (args.k*rho)**args.k / (math.factorial(args.k)*(1-rho))
p0 = 1 / (p1 + p2)
expectWait = ((args.arrR/args.serR)**args.k * args.serR / (math.factorial(args.k-1)*(args.k*args.serR - args.arrR)**2))*p0
expectTime = expectWait + 1/args.serR
expectCustomer_inSys = expectTime * args.arrR

# expWait_v1 = ((args.arrR/args.serR)**args.k / (math.factorial(args.k)*(args.k*args.serR)*(1-args.arrR/(args.k*args.serR))**2))*p0

print(round(avgWait,5),'[average wait]')
print(round(expectWait,5),'[expect wait]')
print(round(avgCustomer_inSys, 3),'[average customer in system]')
print(round(expectCustomer_inSys, 3),'[expect customer in system]')