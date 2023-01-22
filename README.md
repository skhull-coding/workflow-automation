# project.py
### Main File of the project

## What it does?
#### Manage Files by making a copy of the file in the predefined save directory.
#### if by chance the main file is lost, the file in the save directory still remains. (Maximum chances if the data is on a usb drive or remote location)
#### this code can be changed later for remote filesystem if possible
#### this project also adds autosave feature that detects if the file changed and if it changed then updates the file in the save location
#### this is implemented in FSM using transitions library

## File Structure:

- project.py - Main file of the code
- workflowfile.py - Contains the class that implements FSM
- const.py - Contains the state and transitions of the implemented FSM
- forDir_incomplete.py - Contains the code for working with folders (Incomplete)

## Directories:

- saveDir - files default save location
- tryDir - Contains files to try the code on

## this code still needs some work