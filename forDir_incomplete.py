# Incomplete




# Important Imports
from transitions import Machine
from os import path, walk, makedirs, mkdir, getcwd
import shutil
from asyncio import create_task, get_event_loop, sleep, gather, run
from const import workflowStates as machineStates, workflowTransitions as machineTransitions


class WorkflowFolder(object):
    def __init__(self, folder_name, save_location) -> None:

        # Attributes of the Class Workflow Folder
        self.title = f"Workflow : {folder_name}"
        self.saveLocation = save_location
        self.folderName = folder_name
        self.saveFolder = path.join(
            self.saveLocation, path.basename(self.folderName))

        # Checks if the folder is already in the location
        print("Creating Space for the Workflow.....")
        self.save_data()
        print("Creation Succesful")

        self.autosaveTask = None
        self.checkFolderForAutosaveAfterSecs = 4

        # Initialization of the Machine
        self.workflow = Machine(
            self, states=machineStates, transitions=machineTransitions, initial='powerOff')

    def save_data(self):
        """Saves the Folder to the Desired Location"""
        if path.exists(self.saveFolder):
            shutil.rmtree(self.saveFolder)
        shutil.copytree(self.folderName, self.saveFolder,
                        symlinks=False, copy_function=shutil.copy2)

    def autosave_on(self):
        """Start the autosave task/turns on the autosave feature"""
        self.autosaveTask = create_task(self.autosave())
        print("Autosave feature is turned on")

    def autosave_off(self):
        """Cancels the autosave task/turns off the autosave feature"""
        self.autosaveTask.cancel()

    async def autosave(self):
        """Saves folder after some set interval of seconds infinitely until cancelled"""
        while True:
            if self.autosaveTask and self.autosaveTask.cancelled():
                print("Autosave feature is turned off")
                return
            # temporary solution for not crashing the code
            await sleep(self.checkFolderForAutosaveAfterSecs)
            self.save_data()

    def on_enter_inProgress(self):
        """Runs on entering the `inProgress` state"""
        self.show_workflow_state()
        self.save_data()

    def on_enter_inSaveProgress(self):
        """Runs on entering the `inSaveProgress` state"""
        self.show_workflow_state()
        self.autosave_on()

    def on_exit_inSaveProgress(self):
        """Runs to exiting the `inSaveProgress` state"""
        print("Autosave feature is turned off")
        self.autosave_off()

    def on_enter_idle(self):
        """Runs on entering the `idle` state"""
        self.show_workflow_state()

    def on_enter_powerOff(self):
        """Runs on entering the `powerOff` state"""
        self.workflow.remove_model(self)
        self.show_workflow_state()
        print("Workflow Ended")
        exit(1)

    def show_workflow_state(self):
        """Prints the Workflow state"""
        print(f"Workflow State : {self.state}")

    def say_saved(self):
        print("Saved")


def runWorkflowFunc(workflow, transition):
    """Runs the transitions of the workflow"""
    try:
        workflow.trigger(transition)
        return True
    except:
        print(f"Workflow can't transition.")
        return False


async def takeInput(workflow):
    """Inputs user to change the state of the Workflow"""
    while True:
        value = await get_event_loop().run_in_executor(None, input)
        if not runWorkflowFunc(workflow, value):
            break


async def main(folder_name, save_location):
    """Main Function for the code"""
    workflow = WorkflowFolder(folder_name, save_location)
    await gather(takeInput(workflow))

if __name__ == "__main__":
    run(main(getcwd(), r"E:\Project Files"))
