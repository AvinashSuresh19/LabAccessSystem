#!/usr/bin/python3
#this file handles the scanning for swipes
#time is synced at 8pm and anyone who hasnt swiped out is removed.
import time
import logging
import logging.handlers
import socket
import requests
import json
import urllib.request
import xml.etree.ElementTree as ET
import datetime
import os
#Setup logging
handler = logging.handlers.WatchedFileHandler(os.environ.get("LOGFILE", "/home/tc/sshreader_errors.log"))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)
#Local files (in same dir)
import syncTime
debugMode = False
PORTDB_IP = '10.131.81.38'
PORTDB_PORT = 6060
#Following times are UTC scheduled
TIME_USERLIST_WIPE_HR = 70
TIME_USERLIST_WIPE_MN = 0
TIME_TIMESYNC_HR = 70
TIME_TIMESYNC_MN = 0
TIME_REBOOT_HR = 6
TIME_REBOOT_MN = 0
#print that we have completed startup operations to log
logging.info("sshreader.py launched successfully")
lastHeartbeat = 'Never'
#log down to the heartbeat after an error has occured if 1
intenseLogging = 0

def checkTempUser(pNum):
    req = urllib.request.Request("http://127.0.0.1:8000/userTempData/?format=json")
    r = urllib.request.urlopen(req).read()
    cont = json.loads(r.decode('utf-8'))
    for item in cont:
        #print(item['fname'], item['lname'], item['personalNo'])
        #print(pNum)
        if(item['personalNo'] == pNum):
            return True
    return False
def checkUser(pNum):
    req = urllib.request.Request("http://127.0.0.1:8000/userData/?format=json")
    r = urllib.request.urlopen(req).read()
    cont = json.loads(r.decode('utf-8'))
    for item in cont:
        #print(item['fname'], item['lname'], item['personalNo'])
        #print(pNum)
        if(item['personalNo'] == pNum):
            return True
    return False
def getDelUrl(pNum,pfname,plname):
    #swipe out url
    #only suplly first name + lastname  or  pNum
    req = urllib.request.Request("http://127.0.0.1:8000/userData/?format=json")
    r = urllib.request.urlopen(req).read()
    cont = json.loads(r.decode('utf-8'))
    for item in cont:
        #print(item['fname'], item['lname'], item['personalNo'])
        if(item['personalNo'] == pNum):
            return item['url']
        if(item['fname'] == pfname and item['lname'] == plname):
            return item['url']
    return ' '
def reportError():
    values = {'title': 'Connectivity Problem Detected', 'description': 'A necessary connection has been terminated.<br><br>Contact a system administrator to repair the system.', 'newstype': 'warning'}
    r = requests.post('http://127.0.0.1:8000/news/', data=values)
    print('[POST]')
    #force doors open
    #http://10.131.81.49/stateFull.xml?relayState=2
    try:
        doorIP = "10.131.81.48"
        r = urllib.request.urlopen("http://" + doorIP + "/stateFull.xml?relayState=2", timeout=2000)
        doorIP = "10.131.81.49"
        r = urllib.request.urlopen("http://" + doorIP + "/stateFull.xml?relayState=2", timeout=2000)
    except Exception:
        print("UI Print ERROR exception occured")
        logging.info("UI Print ERROR exception occured")
def addPerson(strFName,strLName,strFrom,strTo,strPersonalNo,strDateTime,strDepartment):
    #auth=('secpi', 'RpiSECrand123$$')
    if(strFrom == '95' or strFrom == '33'):
        #swipe out
        c = checkTempUser(strPersonalNo)
        d = checkUser(strPersonalNo)
        if(c or d):
            #User already swiped
            print('Already Swiped')
            if(d):
                #already on board
                print('Reopening door')
                openDoor(strFrom)
        else:
            values = {'date_time': strDateTime, 'fname': strFName, 'lname': strLName, 'entry': strFrom, 'exit': strTo, 'personalNo': strPersonalNo, 'department': strDepartment}
            r = requests.post('http://127.0.0.1:8000/userTempData/', data=values)
            print('[POST]')
    else:
        #swiping back in
        if(strPersonalNo  == "No ID No."):
            d = getDelUrl('randomvaluenonecouldhave', strFName, strLName)
        else:
            d = getDelUrl(strPersonalNo, ' ', ' ')
        if(d != ' '):
            r = requests.delete(d)
            openDoor(strFrom)
            print('[DELETE]')
        else:
            #temporary swipe for those who are not on the board
            openDoor(strFrom)
            print('[DELETE] Entry Not found in DB!')
def openDoor(doorLoc):
    #opens door
    doorIP= ""
    if(doorLoc == "32" or doorLoc == "33"):
        doorIP = "10.131.81.48"
        print("Opening Downstairs Door")
    else:
        doorIP = "10.131.81.49"
        print("Opening Upstairs Door")
    r = urllib.request.urlopen("http://" + doorIP + "/stateFull.xml?relayState=2&pulseTime=10", timeout=2000)

def deleteAllUsers():
    #delete everything on the users list
    req = urllib.request.Request("http://127.0.0.1:8000/userData/?format=json")
    r = urllib.request.urlopen(req).read()
    cont = json.loads(r.decode('utf-8'))
    for item in cont:
        print('DELETING: ' + item['fname'], item['lname'], item['personalNo'])
        if(item['url'] != ' '):
            r = requests.delete(item['url'])
def updateSystemTime():
    #update system clock so that every db entry is accurate
    print('Time Sync: Calling external python file')
    syncTime.syncTime()
    print('Time Sync Complete')
def validateStr(strIn, maxAllowableLen):
    #send string to this function it will truncate names that are too long for django
    if(strIn == None):
        return None
    if(len(strIn)< maxAllowableLen):
        maxAllowableLen = len(strIn)
    return strIn[0:maxAllowableLen]
def decodeXml(xmlString):
    global lastHeartbeat
    global intenseLogging
    if(debugMode == True):
        print("New Data Received.");
    try:
        root = ET.fromstring(xmlString)
        for item in root.findall('Heartbeat'):
            print("Heartbeat Received")
            lastHeartbeat = str(datetime.datetime.now().time())
            if(intenseLogging == 1):
                logging.info("UTC time: " + str(datetime.datetime.now().time()))
                logging.info("Last Heartbeat: " + lastHeartbeat)
            #check times if time is right then wipe
            if(debugMode):
                print(datetime.datetime.now())
            x = datetime.datetime.utcnow() #hour can be less than zero. Im not checking
            if(x.hour == TIME_USERLIST_WIPE_HR and x.minute == TIME_USERLIST_WIPE_MN and x.year != 1970):
                #clear list. This wil run multiple times in the minute It will be called. This action is not a problem right now..
                print('Delete All Users Scheduled Task Initiated')
                deleteAllUsers()
            if(x.hour == TIME_TIMESYNC_HR and x.minute == TIME_TIMESYNC_MN and x.year != 1970):
                #set time
                print('Update System Time')
                updateSystemTime()
            if(x.hour == TIME_REBOOT_HR and x.minute == TIME_REBOOT_MN and x.year != 1970):
                print('Rebooting')
                os.system('sudo reboot')
        for item in root.findall('Acccess'):
            fname = validateStr(item.get('firstname'),25)
            lname = validateStr(item.get('lastname'),25)
            entry = item.get('from')
            exit = item.get('to')
            action = item.get('action')
            dept = validateStr(item.get('dept'),20)
            personalNo = validateStr(item.get('personalNo'),10)
            dateTime = item.get('date') + ' ' + item.get('time')
            if(dept == None):
                if(debugMode):
                    print('No Department')
                dept = "No Department"
            if(personalNo == None):
                if(debugMode):
                    print('No PersonalNo')
                personalNo  = "No ID No."
            if(action == 'success'):
                print(dateTime, ' ', fname, lname, personalNo, dept, entry, exit)
                addPerson(fname,lname,entry,exit,personalNo,dateTime,dept)
                if(intenseLogging == 1):
                    logging.info("User Swiped: " + lname)
                    logging.info("UTC time: " + str(datetime.datetime.now().time()))
                    logging.info("Last Heartbeat: " + lastHeartbeat)
            else:
                print("User with no access attempted swipe: ", dateTime, ' ', fname, lname, personalNo, dept, entry, exit)
    except Exception:
        intenseLogging = 1
        print("ERROR: failure decoding XML")
        logging.info("ERROR: failure decoding XML")
        logging.info("UTC time: " + str(datetime.datetime.now().time()))
        logging.info("Last Heartbeat: " + lastHeartbeat)
        logging.info("START XMLSTRING")
        logging.info(xmlString)
        logging.info("END XMLSTRING")
        logging.exception("XML parse error")
        reportError()
while True:
    xmlItem = ""
    try:
        xmlItem = ""
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((PORTDB_IP, PORTDB_PORT))
        while 1:
            data = client_socket.recv(768)
            #was 512
            if ( data == 'q' or data == 'Q'):
                client_socket.close()
                break;
            else:
                xmlItem = data.strip()
                if(debugMode == True):
                    print("RECIEVED:" , data)
                    print(xmlItem)
                    print("END")
                #call REST
                if b'TimingsList' in xmlItem:
                    print("TIMINGS LIST")
                else:
                    decodeXml(xmlItem)
        client_socket.close()
    except Exception:
        intenseLogging = 1
        print("ERROR EVENT")
        logging.info("ERROR EVENT")
        logging.info("UTC time: " + str(datetime.datetime.now().time()))
        logging.info("Last Heartbeat: " + lastHeartbeat)
        logging.info("START XMLITEM")
        logging.info(xmlItem)
        logging.info("END XMLITEM")
        logging.exception("Error (pausing for 5s)")
        reportError()
        time.sleep(5)
