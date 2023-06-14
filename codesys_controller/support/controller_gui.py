import tkinter as tk


class MyGui:
    def __init__(self, controller_object):
        self.window = tk.Tk()
        self.window.title("VM Controller")
        self.window.geometry("300x900")

        self.controller_object = controller_object

        self.label_objects_list = []
        self.button_objects_list = []
        self.command_entry = None

        # get the names of the methods in the controller object
        self.criteria = lambda meth: not meth.startswith('_') \
                                     and type(getattr(self.controller_object, meth)) == \
                                     type(self.controller_object.print_list_of_vms)
        self.list_of_names = [str(meth) for meth in dir(self.controller_object) if self.criteria(meth)]
        # create a label and button for each method
        [self.create_label_and_button(function_name) for function_name in self.list_of_names]

    def create_label_and_button(self, function_name):
        vm_function = getattr(self.controller_object, function_name)

        label = tk.Label(self.window, text=function_name, font=("Arial", 12))
        label.pack(pady=5)
        self.label_objects_list.append(label)

        button = tk.Button(self.window, text=">", command=vm_function, font=("Arial", 12))
        button.pack(pady=10)
        self.button_objects_list.append(button)

    def start(self):
        self.window.mainloop()
