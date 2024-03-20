# Tasking

## People
- Alex Lueddecke
- Kyle Fowler

## Overall
- Create README file
- Script to quickly compile .csv data

## Scale Firmware
### To Do:
- Add debug functionality to be outputed to UI
    - Main focus currently is sending leg values (in units)
    - Needs to receive serial message to activate (currently thinking 'd')


## Scale UI
### To Do:
- Build information view
- Add debug view to allow for load value views for each individual leg - Kyle
    - new output delimited with ":"
    - Add the 4 values together to get total weight
    - open debug view as separate window
    - Requires firmware adjustments
    - 
- Checklist Items
        - Verify that data uploading is set to true
        - Connect Serial Port
        - Verify Output File
        - Calibrate
        - Connect to Wifi
- Start up checklist (use info view?)
- default values for specific style guide items (if they are needed)
- Windows compatiability, looks weird, style guide revision
- Arduino Disconnect issue
    - ERROR CODE: 	File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/serial/serialposix.py", line 581, in read raise SerialException('read failed: {}'.format(e)) serial.serialutil.SerialException: read failed: [Errno 6] Device not configured
- Scale number parameter uploaded to firebase
    - allow for two seperate scale systems
    - Maybe pull device ID
- Resolve Requirments.txt file
- Known weight checker display - Kyle
    - make window display on side and show the expected weight in debug mode
    - allows the user to place a known weight along with the unknown to verify that the reading is accurate
    - e.g. is your reading is 100lb and you add a 25lb weight your output should change to reflect 125
    - More of a debugging task but wanted to capture idea
- Configurable rounding on Scale UI rather that arduino 
    





