import os
import subprocess
from os.path import join
from pathlib import Path


# ==============================================================================
# Utilities
# ==============================================================================
class Utilities():
    '''
    '''
# |----------------------------------------------------------------------------|
# Class Variables
# |----------------------------------------------------------------------------|
    def __init__(self):
        pass
# |----------------------End of get_script_name--------------------------------|

# |----------------------------------------------------------------------------|
# get_home_path
# |----------------------------------------------------------------------------|
    def get_home_path(self):
        return str(Path.home())

# |----------------------End of get_home_path---------------------------------|

# |----------------------------------------------------------------------------|
# get_app_path
# |----------------------------------------------------------------------------|
    def get_app_path(self):
        return str(Path.home())

# |----------------------End of get_app_path----------------------------------|

# |----------------------------------------------------------------------------|
# get_scripts_path
# |----------------------------------------------------------------------------|
    def get_scripts_path(self):
        home_path = self.get_home_path() 
        return join(home_path, "Documents", "wsi_startup_scripts")

# |----------------------End of get_scripts_path------------------------------|

# |----------------------------------------------------------------------------|
# change_directory
# |----------------------------------------------------------------------------|
    def change_directory(self, path):
        os.chdir(path)
# |----------------------End of change_directory------------------------------|

# |----------------------------------------------------------------------------|
# is_port_exists
# |----------------------------------------------------------------------------|
    def is_port_exists(self, port):
        status = False
        cmd = "lsof -i:{}".format(port)
        try:
            status = self.get_subprocess_result_status(cmd)
        except Exception as error_msg:
            self.get_error_info(error_msg)
        return status
# |----------------------End of is_port_exists--------------------------------|

# |----------------------------------------------------------------------------|
# get_subprocess_result_status
# |----------------------------------------------------------------------------|
    def get_subprocess_result_status(self, cmd):
        status = False
        check = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
        result = check.stdout.read()

        if len(result) > 0:
            status = True
        return status

# |----------------------End of get_subprocess_result_status------------------|
