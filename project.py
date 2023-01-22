# Important Imports
from sys import argv
from os import getcwd, path, mkdir
from asyncio import run
from workflowfile import main

# Some Constants
currentDir = getcwd()
saveDir = path.join(currentDir, "saveDir")
if not path.exists(saveDir):
    mkdir(saveDir)


# Functions for Managing Files and Folders

def check_path(file_name):
    """Check if the file exists or not. 
    if not then throws File not found error"""
    if not path.exists(file_name):
        raise FileNotFoundError(f"No Path Exists with {file_name}")
    else:
        return True


def manage_file_workflow(file_name):
    """Function for managing the File Workflow"""
    run(main(file_name, saveDir))


def manage_dir_workflow(dir_name):
    """Still Incomplete"""
    print("Not implemented right Now!")


if __name__ == "__main__":

    # Getting Delimiter for Application
    try:
        delimiter = argv[1]
    except IndexError:
        raise RuntimeError("No Delimiter was found")

    # Specific use case for delimiter type
    match delimiter:
        case '-f':
            # print("This is for Managing a single File")
            if check_path(argv[2]):
                manage_file_workflow(argv[2])
        case '-d':
            # print("This is for Managing Directory")
            if check_path(argv[2]):
                manage_dir_workflow(argv[2])
        case 'start':
            # print("This is for Managing the Same Directory the Program has Ran in")
            manage_dir_workflow(currentDir)
        case _:
            raise RuntimeError("No use case for '"+argv[1]+"' found")
