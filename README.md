# project.py
### Main File of the project

## What it does?
#### Manage Files by making a copy of the file in the predefined save directory.
#### if by chance the main file is lost, the file in the save directory still remains. (Maximum chances if the data is on a usb drive or remote location)
#### this code can be changed later for remote filesystem if possible
#### this project also adds autosave feature that detects if the file changed and if it changed then updates the file in the save location
#### this is implemented in FSM using transitions library

## How to use?
### Type this command to open the program (make sure python is installed on you system)
- python project.py -f <file-name> (type the file-name where <file-name> is located, if the file is outside the parent dir then give file-name with its location)
- #### like - python project.py -f project.py (will create a copy of project.py inside the saveDir folder of this repo)
- #### after the program runs,
- type 'on' to get the state of workflow to change to 'idle'
- type 'start' to get the state of the workflow to 'inProgress' (now you can save the data after typing 'save' every time you want to save the data)
- you can also type 'autosave' to save the file whenever it gets updated (you can turn off the autosave mode after typing 'autosave' again or 'autosaveoff' instead)
- after you finish working on file, type 'finish' to get to the 'idle' state again.
- you can then type 'off' to get to the 'Power off' state of the workflow ( this will end the program )
- #### - if you entered in the wrong order, the workflow will stop. (program will exit)

## File Structure:

- project.py - Main file of the code
- workflowfile.py - Contains the class that implements FSM
- const.py - Contains the state and transitions of the implemented FSM
- forDir_incomplete.py - Contains the code for working with folders (Incomplete)

## Directories:

- saveDir - files default save location
- tryDir - Contains files to try the code on

## this code still needs some work
