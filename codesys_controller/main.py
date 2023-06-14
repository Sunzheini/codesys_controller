# The usage of the CODESYS functionalities requires python 2.7 (f-strings not working)

from __future__ import print_function
import sys

from codesys_controller.support.codesys_controller_class import CodesysController
from codesys_controller.support.controller_gui import MyGui


# ----------------------------------- custom variables -----------------------------------

library_path = "C:\\Users\\BG0DZRV\\Documents\\Projects\\Libs\\AutomatedTestingPtP.library"
project_path = sys.argv[1]                      # auto get from .bat file

cmmt_as_device_name = 'CMMT-AS'
cmmt_st_device_name = 'CMMT-ST'
cmmt_as_device_version = cmmt_st_device_version = sys.argv[2]  # auto get from .bat file

device_name_in_project = 'CMMT_AS_Rot'
drives_list_in_project = ["CI_TestRotaryAxis_CMMT_AS", ]


# ---------------------------------------- no gui ----------------------------------------
# print("----------------------------------- START OF SCRIPT --------------------------------")
# codesys_controller = CodesysController()
# codesys_controller.run_test_sequence()
# print("------------------------------------ END OF SCRIPT ---------------------------------")


# --------------------------------------- with gui ---------------------------------------
if __name__ == '__main__':
    codesys_controller = CodesysController()
    gui_window = MyGui(codesys_controller)  # create gui and pass the vm object to the gui
    gui_window.start()      # start the gui
