import time
import os
import ntplib
TIMESERVER_IP = '10.131.192.9'
def syncTime():
    print('Attempting to sync time with ' + TIMESERVER_IP)
    os.environ['TZ'] = 'EST+05EDT,M4.1.0,M10.5.0'
    time.tzset()
    try:
        client = ntplib.NTPClient()
        response = client.request(TIMESERVER_IP)
        os.system('date ' + time.strftime('%m%d%H%M%Y.%S',time.localtime(response.tx_time)))
        print('SUCCESS Syncing time with ' + TIMESERVER_IP)
    except:
        print('ERROR Syncing time with ' + TIMESERVER_IP)
