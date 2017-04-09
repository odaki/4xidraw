# grbl_motion.py
# Motion control utilities for GRBL
#
# The MIT License (MIT)
# 
# Copyright (c) 2016 Evil Mad Scientist Laboratories
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import grbl_serial
import inkex

class GrblMotion(object):
        def __init__(self, portName, stepsPerInch, penUpPosition, penDownPosition):
                self.portName = portName
                self.stepsPerInch = stepsPerInch
                self.penUpPosition = penUpPosition
                self.penDownPosition = penDownPosition
                
        def IsPausePressed(self):
	        if (self.portName is not None):
		        return False; # TODO

        def sendPenUp(self, PenDelay):
	        if (self.portName is not None):
		        strOutput = 'M3 S' + str(self.penUpPosition) + '\rG4 P' + str(PenDelay) + '\r'
		        grbl_serial.command(self.portName, strOutput)

        def sendPenDown(self, PenDelay):
	        if (self.portName is not None):
		        strOutput = 'M3 S' + str(self.penDownPosition) + '\rG4 P' + str(PenDelay) + '\r'
		        grbl_serial.command(self.portName, strOutput)

        def doXYAccelMove(self, deltaX, deltaY, vInitial, vFinal):
	        # Move X/Y axes as: "AM,<initial_velocity>,<final_velocity>,<axis1>,<axis2><CR>"
	        # Typically, this is wired up such that axis 1 is the Y axis and axis 2 is the X axis of motion.
	        # On EggBot, Axis 1 is the "pen" motor, and Axis 2 is the "egg" motor.
	        # Note that minimum move duration is 5 ms.
	        # Important: Requires firmware version 2.4 or higher.
	        if (self.portName is not None):
		        strOutput = '' #!!','.join(['AM', str(vInitial), str(vFinal), str(deltaX), str(deltaY)]) + '\r'
		        grbl_serial.command(self.portName, strOutput)

        def doXYMove(self, deltaX, deltaY, duration):
	        # Move X/Y axes as: "SM,<move_duration>,<axis1>,<axis2><CR>"
	        # Typically, this is wired up such that axis 1 is the Y axis and axis 2 is the X axis of motion.
	        # On EggBot, Axis 1 is the "pen" motor, and Axis 2 is the "egg" motor.
	        if (self.portName is not None):
                        moveX = deltaX/self.stepsPerInch*25.4
                        moveY = deltaY/self.stepsPerInch*25.4
                        maxMove = max(moveX, moveY)
                        rate = int(maxMove/(duration/60000.0))
		        strOutput = 'F ' + str(rate) + ' X '+str(moveX) + ' Y '+str(moveY) + '\r'
			#inkex.errormsg(strOutput)
		        grbl_serial.command(self.portName, strOutput)

        def doABMove(self, deltaA, deltaB, duration):
	        # Issue command to move A/B axes as: "XM,<move_duration>,<axisA>,<axisB><CR>"
	        # Then, <Axis1> moves by <AxisA> + <AxisB>, and <Axis2> as <AxisA> - <AxisB>
	        if (self.portName is not None):
		        strOutput = '' #!! ','.join(['XM', str(duration), str(deltaA), str(deltaB)]) + '\r'
		        grbl_serial.command(self.portName, strOutput)				
