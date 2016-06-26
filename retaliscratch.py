#!/usr/bin/python
#
# From: RETALIATION - A Jenkins "Extreme Feedback" Contraption
# https://github.com/codedance/Retaliation

# Copyright 2011 PaperCut Software Int. Pty. Ltd. http://www.papercut.com/

# Modifications Copyright 2013 Nathan Byrd
# Modified to connect to Scratch using Remote Sensor Connections protocol.

#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# 



##############################################################################
#
# Retaliscratch - operate missile launcher from Scratch
# http://scratch.mit.edu
#
# Install prerequisites: pip install scratchpy pyusb
#
# To use:
# 1) Start Scratch, enable Remote Sensor Connections.
#    See: http://wiki.scratch.mit.edu/wiki/Remote_Sensor_Connections
# 2) Execute: sudo python retaliscratch.py
# 3) Use broadcast commands from Scratch:
#    fire X  - fires X missiles
#    reset   - resets to lower left corner
#    up X    - go up for X milliseconds
#    down X  - go down for X milliseconds
#    right X - go right for X milliseconds
#    left X  - go left for X milliseconds
# 4) To shut down, send a keyboard interrupt (Control-C)
##############################################################################

import scratch

import usb.core
import usb.util
import platform
import time
import re

##############################################################################
# Begin original code from RETALIATION: https://github.com/codedance/Retaliation
# Copyright 2011 PaperCut Software Int. Pty. Ltd. http://www.papercut.com/

# Protocol command bytes
DOWN    = 0x01
UP      = 0x02
LEFT    = 0x04
RIGHT   = 0x08
FIRE    = 0x10
STOP    = 0x20

DEVICE = None


def setup_usb():
    # Tested only with the Cheeky Dream Thunder
    global DEVICE
    DEVICE = usb.core.find(idVendor=0x2123, idProduct=0x1010)

    if DEVICE is None:
            raise ValueError('Missile device not found')

    # On Linux we need to detach usb HID first
    if "Linux" == platform.system():
        try:
            DEVICE.detach_kernel_driver(0)
        except Exception, e:
            pass # already unregistered    

    DEVICE.set_configuration()

def send_cmd(cmd):
    DEVICE.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])


def send_move(cmd, duration_ms):
    send_cmd(cmd)
    time.sleep(duration_ms / 1000.0)
    send_cmd(STOP)


def run_command(command, value):
    command = command.lower()
    if command == "right":
            send_move(RIGHT, value)
    elif command == "left":
            send_move(LEFT, value)
    elif command == "up":
            send_move(UP, value)
    elif command == "down":
            send_move(DOWN, value)
    elif command == "zero" or command == "park" or command == "reset":
            # Move to bottom-left
        send_move(DOWN, 2000)
        send_move(LEFT, 8000)
    elif command == "pause" or command == "sleep":
            time.sleep(value / 1000.0)
    elif command == "fire" or command == "shoot":
        if value < 1 or value > 4:
            value = 1
        # Stabilize prior to the shot, then allow for reload time after.
        time.sleep(0.5)
        for i in range(value):
            send_cmd(FIRE)
            time.sleep(4.5)
    else:
            print "Error: Unknown command: '%s'" % command

# End source from RETALIATION
# Removed usage and hutson code
##############################################################################


##############################################################################
# Begin code for retaliscratch
# By: Nathaniel Byrd

# Listen for commands from scratch
def listen():
    while True:
        try:
           yield s.receive()
        except scratch.ScratchError:
           raise StopIteration

# Setup USB to talk to missile launcher using RETALIATION
setup_usb()

# Start scratch
s = scratch.Scratch()

# Loop listening for a message to handle
try:
    for msg in listen():
        if msg[0] == 'broadcast':
            # look for word, followed optionally by a space and number
            matchObj = re.match('^(\w+)(\s+(\d+))?$', msg[1], re.M|re.I)
            if matchObj:
                try:
                    # execute the RETALIATION command on the broadcast message
                    run_command(matchObj.group(1), int(matchObj.group(2)) if matchObj.group(2) != None else 0)
		    s.broadcast('DONE ' + msg[1])
                except ValueError:
                    print "Bad value for command"
except KeyboardInterrupt:
    print "Keyboard interrupt, resetting and shutting down..."
    run_command('reset', 0)
    s.disconnect()

##############################################################################
