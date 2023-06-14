import time

from codesys_controller.support.control_methods_collection import Collection
from codesys_controller.main import library_path, cmmt_as_device_name, cmmt_as_device_version, \
    cmmt_st_device_name, cmmt_st_device_version, project_path, device_name_in_project
from codesys_controller.support.test_cases_collection import TEST_CASES


# -------------------------------- controller class ---------------------------------------
class CodesysController:
    def __init__(self):
        self.repository = None
        self.installed_library = None
        self.all_devices_object = None
        self.device_object_cmmt_as = None
        self.device_details_cmmt_as = None
        self.device_object_cmmt_st = None
        self.device_details_cmmt_st = None
        self.current_project = None
        self.device_in_project = None
        self.device_details_in_project = None
        self.online_app = None

    def get_objects(self):
        self.repository = Collection.select_repository(repository_number=0)
        self.installed_library = Collection.install_library(library_path, self.repository)
        self.all_devices_object = Collection.get_all_devices_object()

    def check_cmmt_as_device_version(self):
        self.device_object_cmmt_as = Collection.get_device_object_by_name_and_version(
            cmmt_as_device_name,
            cmmt_as_device_version,
            self.all_devices_object,
        )
        self.device_details_cmmt_as = Collection.get_device_details(self.device_object_cmmt_as)

    def check_cmmt_st_device_version(self):
        self.device_object_cmmt_st = Collection.get_device_object_by_name_and_version(
            cmmt_st_device_name,
            cmmt_st_device_version,
            self.all_devices_object,
        )
        self.device_details_cmmt_st = Collection.get_device_details(self.device_object_cmmt_st)

    def open_project(self):
        self.current_project = Collection.open_project(project_path)

    def find_device_in_project_cmmt_as_rot(self):
        self.device_in_project = Collection.find_device_in_project(self.current_project,
                                                                   device_name_in_project)
        self.device_details_in_project = Collection.get_device_in_project_details(self.device_in_project)

        old_device_before_update = self.device_in_project
        self.device_in_project = Collection.check_device_version(self.device_in_project,
                                                                 self.device_object_cmmt_as)

        if old_device_before_update != self.device_in_project:
            self.save_project()
            self.close_project()

    def save_project(self):
        Collection.save_project(self.current_project)

    def close_project(self):
        Collection.close_project(self.current_project)

    def create_online_application(self):
        self.online_app = Collection.create_online_application(self.online_app)

    def login(self):
        self.online_app = Collection.login(self.online_app)

    def logout(self):
        self.online_app = Collection.logout(self.online_app)

    def reset_warm(self):
        self.online_app = Collection.reset_warm(self.online_app)

    def run_application(self):
        self.online_app = Collection.run_application(self.online_app)

    def run_tests(self):
        tests = (
            TEST_CASES["11"],
        )

        self.online_app = Collection.run_tests(self.online_app, *tests)

    def run_test_sequence(self):
        self.get_objects()
        self.check_cmmt_as_device_version()
        self.check_cmmt_st_device_version()
        self.open_project()
        self.find_device_in_project_cmmt_as_rot()
        self.create_online_application()

        self.login()
        time.sleep(10)

        self.reset_warm()
        time.sleep(10)

        self.run_application()
        time.sleep(20)

        self.run_tests()
        time.sleep(20)

        self.logout()
        time.sleep(10)

        self.close_project()
