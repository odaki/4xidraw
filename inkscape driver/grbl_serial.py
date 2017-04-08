# grbl_serial.py
# Serial connection utilities for RAMPS

import serial, time
import inkex
import gettext

def findPort():	
    # Find a GRBL board connected to a USB port.
    try:
	from serial.tools.list_ports import comports
    except ImportError:
	comports = None		
	return None
    if comports:
	comPortsList = list(comports())
	for port in comPortsList:
	    if port[1].startswith("USB2.0-Serial"): # Works for Ubuntu
		return port[0]
    return None

def testPort(comPort):
    '''
    Return a SerialPort object for the first port with a GRBL board.
    YOU are responsible for closing this serial port!
    '''		
    if comPort is not None:
	try:
	    serialPort = serial.Serial(comPort, baudrate = 115200, timeout = 1.0,
                                       rtscts = False,
                                       dsrdtr = True)
            serialPort.write('$I\r')
            time.sleep(1)
	    strVersion = serialPort.readline()
	    if strVersion and strVersion.startswith('Grbl'):
		return serialPort
            serialPort.write('$I\r')
            time.sleep(1)
	    strVersion = serialPort.readline()
	    if strVersion and strVersion.startswith('Grbl'):
		return serialPort
	    serialPort.close()
	except serial.SerialException:
	    pass
	return None
    else:
	return None

def openPort():
    foundPort = findPort()
    serialPort = testPort(foundPort)
    if serialPort:
	return serialPort
    return None

def closePort(comPort):
    if comPort is not None:
	try:
	    comPort.close()
	except serial.SerialException:
	    pass

def query(comPort, cmd):
    if (comPort is not None) and (cmd is not None):
	response = ''
	try:
	    comPort.write(cmd)
	    comPort.write(cmd)
	    response = comPort.readline()
	    nRetryCount = 0
	    while (len(response) == 0) and (nRetryCount < 100):
		# get new response to replace null response if necessary
		response = comPort.readline()
		nRetryCount += 1
	    if cmd.strip().lower() not in ["v","i","a", "mr","pi","qm"]: #!!
		# Most queries return an "OK" after the data requested.
		# We skip this for those few queries that do not return an extra line.
		unused_response = comPort.readline() # read in extra blank/OK line
		nRetryCount = 0
		while (len(unused_response) == 0) and (nRetryCount < 100):
		    # get new response to replace null response if necessary
		    unused_response = comPort.readline()
		    nRetryCount += 1
	except:
	    inkex.errormsg(gettext.gettext("Error reading serial data."))
	return response
    else:
	return None

def command(comPort, cmd):
    if (comPort is not None) and (cmd is not None):
	try:
	    comPort.write(cmd)
	    response = comPort.readline()
	    nRetryCount = 0
	    while (len(response) == 0) and (nRetryCount < 100):
		# get new response to replace null response if necessary
		response = comPort.readline()
		nRetryCount += 1
		if response.strip().startswith("OK"):
		    pass  # 	inkex.errormsg( 'OK after command: ' + cmd ) #Debug option: indicate which command.
		else:
		    if (response != ''):
			inkex.errormsg('Error: Unexpected response from GRBL.') 
			inkex.errormsg('   Command: ' + cmd.strip())
			inkex.errormsg('   Response: ' + str(response.strip()))
		    else:
			inkex.errormsg('GRBL Serial Timeout after command: ' + cmd)
	except:
	    inkex.errormsg( 'Failed after command: ' + cmd )
	    pass 

if __name__ == "__main__":
    p = findPort()
    print("Found port %s" % p)
    p = testPort(p)
    print("Tested port %s" % p)
    
