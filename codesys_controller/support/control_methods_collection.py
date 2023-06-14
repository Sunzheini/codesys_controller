import datetime
import time

from codesys_controller.support.custom_decorators import print_method_name_time_and_result
from codesys_controller.support.test_cases_collection import TEST_CASES
from codesys_controller.support.codesys_objects import codesys_library_manager, codesys_device_repository, \
        codesys_project_object, codesys_online_object, codesys_online_change_option, \
        codesys_reset_option, codesys_application_state_object
from codesys_controller.main import cmmt_as_device_version, drives_list_in_project


# -------------------- collection of methods to control codesys --------------------------
class Collection:
    @staticmethod
    @print_method_name_time_and_result
    def select_repository(repository_number=0):
        repo = codesys_library_manager.repositories[repository_number]
        return repo

    @staticmethod
    @print_method_name_time_and_result
    def install_library(libpath, repo, overwrite=True):
        installed_lib = codesys_library_manager.install_library(libpath, repo, overwrite=overwrite)
        return installed_lib

    @staticmethod
    @print_method_name_time_and_result
    def get_all_devices_object():
        devices_obj = codesys_device_repository.get_all_devices()
        return devices_obj

    @staticmethod
    @print_method_name_time_and_result
    def get_device_object_by_name_and_version(device_name, device_version, all_dev_object):
        devices = all_dev_object
        for device in devices:
            if device_name in device.device_info.name and device.device_id.version == device_version:
                return device
        print("Device Not Found")
        return None

    @staticmethod
    @print_method_name_time_and_result
    def get_device_details(device):
        try:
            return "Device Name: {}\nDevice Version: {}\nDevice Type: {}" \
                   "\nDevice ID: {}\nDevice Vendor: {}\nDevice Description: {}\nDevice Order Nr: {}\n" \
                .format(
                    device.device_info.name,
                    device.device_id.version,
                    device.device_id.type,
                    device.device_id.id,
                    device.device_info.vendor,
                    device.device_info.description,
                    device.device_info.order_number,
                )
        except:
            return "Couldn't get device details"

    @staticmethod
    @print_method_name_time_and_result
    def open_project(path):
        project = codesys_project_object.open(path)
        return project

    @staticmethod
    @print_method_name_time_and_result
    def find_device_in_project(project, device_name, operator=True):
        device = project.find(device_name, operator)

        if Collection._check_if_no_more_than_one_device(device):
            return device
        return None

    @staticmethod
    def _check_if_no_more_than_one_device(device):
        if len(device) > 1:
            print("More than one device found")
            return False
        elif len(device) == 0:
            print("No device found")
            return False
        else:
            return True

    @staticmethod
    @print_method_name_time_and_result
    def get_device_in_project_details(device):
        try:
            return "Device Name: {}\nDevice Type: {}\nDevice ID: {}\nDevice Version: {}\n"\
                .format(
                    device[0].get_name(),
                    device[0].get_device_identification().type,
                    device[0].get_device_identification().id,
                    device[0].get_device_identification().version,
                )
        except:
            return "Couldn't get device details"

    @staticmethod
    @print_method_name_time_and_result
    def check_device_version(device_in_project, device_object):
        if cmmt_as_device_version == device_in_project[0].get_device_identification().version:
            print("Versions are the same: {}".format(cmmt_as_device_version))
            return device_in_project

        if Collection._update_device_version(device_in_project, device_object):
            print("Version updated to: {}".format(cmmt_as_device_version))
        else:
            print("Couldn't update device version")
        return device_in_project

    @staticmethod
    def _update_device_version(device, device_object):
        try:
            device[0].update(
                device_object.device_id.type,
                device_object.device_id.id,
                cmmt_as_device_version,
            )
            return True
        except:
            return False

    @staticmethod
    def save_project(project):
        print("Saving project...")
        project.save()

    @staticmethod
    def close_project(project):
        print("Closing project...")
        project.close()

    @staticmethod
    @print_method_name_time_and_result
    def create_online_application(online_app):
        online_app = codesys_online_object.create_online_application()
        return online_app

    @staticmethod
    @print_method_name_time_and_result
    def login(online_app):
        online_app.login(codesys_online_change_option.Try, True)
        return online_app

    @staticmethod
    @print_method_name_time_and_result
    def logout(online_app):
        online_app.logout()
        return online_app

    @staticmethod
    @print_method_name_time_and_result
    def reset_warm(online_app):
        online_app.reset(codesys_reset_option.Warm, False)
        return online_app

    @staticmethod
    def _check_if_app_state_is_running(online_app):
        if online_app.application_state == codesys_application_state_object.run:
            return True
        return False

    @staticmethod
    @print_method_name_time_and_result
    def run_application(online_app):
        if not Collection._check_if_app_state_is_running(online_app):
            try:
                online_app.start()
                print("Application is running")
            except:
                print("Couldn't run application")
            return online_app

        print("Application is already running")
        return online_app

    @staticmethod
    def _execute_test(online_app, drive, name, timeout):
        print(drive + "." + name, " started at ", time.ctime())
        timeout = time.time() + 60 * timeout

        online_app.set_prepared_value("PLC_PRG." + drive + "." + name + ".Start", "True")
        online_app.write_prepared_values()

        while True:
            bool_done = online_app.read_value("PLC_PRG." + drive + "." + name + ".Done")
            bool_error = online_app.read_value("PLC_PRG." + drive + "." + name + ".Error")
            bool_error_step = online_app.read_value("PLC_PRG." + drive + "." + name + ".ErrorStep")

            if bool_done == 'TRUE':
                print(name, "completed SUCCESSFULLY at ", time.ctime())
                online_app.set_prepared_value("PLC_PRG." + drive + "." + name + ".Start", "False")
                online_app.write_prepared_values()
                return 0

            if bool_error == 'TRUE':
                print("!!")
                print(name, " ERROR occured at ", time.ctime())
                print(name, " ERROR occured at step", bool_error_step)
                print("!!")
                online_app.set_prepared_value("PLC_PRG." + drive + "." + name + ".Start", "False")
                online_app.write_prepared_values()
                return 1

            if time.time() > timeout:  # TimoutError dont work?!
                online_app.set_prepared_value("PLC_PRG." + drive + "." + name + ".Start", "False")
                online_app.write_prepared_values()
                raise ValueError(name + " timeout from phyton script at " + time.ctime())

            time.sleep(1)  # run loop every 500ms

    @staticmethod
    @print_method_name_time_and_result
    def run_tests(online_app, *args):
        error_counter_total = 0
        all_test_dict = {test[0]: test[1] for test in args}

        for drive in drives_list_in_project:
            error_counter = 0

            try:
                print("Test Run: {}".format(drive))
                print("Started at: {}".format(datetime.datetime.now()))

                error_counter = Collection._execute_test(
                    online_app,
                    drive,
                    *TEST_CASES["00"],
                )
                if error_counter > 0:
                    raise ValueError("Initialization of drive failed -- continue with next drive")

                for test in all_test_dict:
                    error_counter = error_counter + Collection._execute_test(
                        online_app,
                        drive,
                        test,
                        all_test_dict[test]
                    )

            except ValueError as e:
                print(str(e))
                error_counter = error_counter + 1
            finally:
                error_counter_total = error_counter_total + error_counter

        return online_app
