retaliscratch
=============

Small project based on RETALIATION to launch foam missiles using Scratch

### From: RETALIATION - A Jenkins "Extreme Feedback" Contraption
<a href="https://github.com/codedance/Retaliation">Retaliation</a>
Copyright 2011 PaperCut Software Int. Pty. Ltd. http://www.papercut.com/

Modifications Copyright 2013 Nathan Byrd
Modified to connect to Scratch using Remote Sensor Connections protocol.

### License

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

### Usage
 1. Start Scratch, enable Remote Sensor Connections.
    See: http://wiki.scratch.mit.edu/wiki/Remote_Sensor_Connections
 2. Execute: sudo python retaliscratch.py
 3. Use broadcast commands from Scratch:
    fire X  - fires X missiles
    reset   - resets to lower left corner
    up X    - go up for X milliseconds
    down X  - go down for X milliseconds
    right X - go right for X milliseconds
    left X  - go left for X milliseconds
 4. To shut down, send a keyboard interrupt (Control-C)
