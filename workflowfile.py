# Important Imports
from transitions import Machine
from os import path
from asyncio import create_task, get_event_loop, sleep, gather, run
from const import workflowStates as machineStates, workflowTransitions as machineTransitions


class WorkflowFile(object):
    def __init__(self, file_name, save_location) -> None:

        # Attributes of the Class Workflow File
        self.title = f"Workflow : {file_name}"
        self.saveLocation = save_location
        self.fileName = file_name
        self.saveFile = path.join(
            self.saveLocation, path.basename(self.fileName))
        self.autosaveTask = None
        self.checkFileForAutosaveAfterSecs = 0.2

        # Checks if the file is already in the location
        # print("Creating Space for File.....")
        try:
            with open(self.saveFile, 'x') as f:
                print("Save Location established")
        except FileExistsError:
            print("File for workflow exists")
        except:
            raise RuntimeError("Couldn't create File")

        # Initialization of the Machine
        self.workflow = Machine(
            self, states=machineStates, transitions=machineTransitions, initial='powerOff')

    def save_data(self):
        """Checks the file data and saves it in the desired file"""
        with open(self.fileName, 'r') as f1, open(self.saveFile, 'r') as f2:
            data_to_save = f1.read()
            data_already = f2.read()
        if data_to_save != data_already:  # checks if the data of the saving file is same as of the workflow file
            with open(self.saveFile, 'w') as f:
                f.write(data_to_save)
            print("Saved")

    def autosave_on(self):
        """Start the autosave task/turns on the autosave feature"""
        self.autosaveTask = create_task(self.autosave())
        print("Autosave feature is turned on")

    def autosave_off(self):
        """Cancels the autosave task/turns off the autosave feature"""
        self.autosaveTask.cancel()

    async def autosave(self):
        """Saves file after some set interval of seconds infinitely until cancelled"""
        while True:
            if self.autosaveTask and self.autosaveTask.cancelled():
                print("Autosave feature is turned off")
                return
            # temporary solution for not crashing the code
            await sleep(self.checkFileForAutosaveAfterSecs)
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


def runWorkflowFunc(workflow, transition):
    """Runs the transitions of the workflow"""
    try:
        workflow.trigger(transition)
        return True
    except:
        print(f"Workflow can't transition.")


async def takeInput(workflow):
    """Inputs user to change the state of the Workflow"""
    while True:
        value = await get_event_loop().run_in_executor(None, input, f"{workflow.title} $ ")
        if not runWorkflowFunc(workflow, value):
            break


async def main(file_name, save_location):
    """Main Function for the code"""
    workflow = WorkflowFile(file_name, save_location)
    await gather(takeInput(workflow))

if __name__ == "__main__":
    run(main(r"./tryDir/text.txt", r"./saveDir"))
