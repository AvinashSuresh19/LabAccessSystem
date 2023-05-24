import time
import os
import ntplib

NETWORKTEST_IP = 'google.com'
def waitInternetConn():
    loopRun = True
    print("Testing Connection With " + NETWORKTEST_IP)
    while loopRun:
        response = os.system("ping -c 1 " + NETWORKTEST_IP)
        if response == 0:
            print(NETWORKTEST_IP, 'is up!')
            loopRun = False
        else:
            print(NETWORKTEST_IP, 'is down!')
        time.sleep(5)

#Start
print("Tower Access System Starting up")
print("1/25/2019")
print("Ryan Bloomgren")
print("-------------------------------")
time.sleep(2)
print('Waiting for the network to come up...')
waitInternetConn()
import syncTime
syncTime.syncTime()
