import os
import subprocess
import json
from os.path import join
from os.path import exists
from pathlib import Path
import requests
import platform


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
        return os.getcwd()

# |----------------------End of get_app_path----------------------------------|

# |----------------------------------------------------------------------------|
# get_scripts_path
# |----------------------------------------------------------------------------|
    def get_scripts_path(self):
        home_path = self.get_home_path() 
        return join(home_path, "Documents", "wsi_startup_scripts")

# |----------------------End of get_scripts_path------------------------------|

# |----------------------------------------------------------------------------|
# get_db_credential_path
# |----------------------------------------------------------------------------|
    def get_db_credential_path(self):
        return join(self.get_app_path(), "config",
                    "database_credentials.json")

# |----------------------End of get_db_credential_path------------------------|

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

# |----------------------------------------------------------------------------|
# read_json
# |----------------------------------------------------------------------------|
    def read_json(self, json_path):
        json_data = {}

        if exists(json_path):
            with open(json_path, 'r') as file:
                json_data = json.loads(file.read())
                file.close()
            return json_data
    
        return json_data
    
# |----------------------End of read_json-----------------------------------------|

# |----------------------------------------------------------------------------|
# send_request_to_host
# |----------------------------------------------------------------------------|
    def send_request_to_host(self, request_json):
        url = request_json["url"]
        params = request_json["params"]
        data = request_json["data"]
        time_out = request_json["time_out"]
        request_type = request_json["request_type"]
        headers = request_json["headers"]
        response = {}
        request_time_out_status = False
        status_code = 500
        print("Url is: {}".format(url))
        
        try:
            if request_type == "POST":
                res = requests.post(url, data=json.dumps(data),headers=headers,
                                    timeout=time_out)
            else:
                res = requests.get(url, params=params, headers=headers,
                                   timeout=time_out)
            print(res.text)
            print(res.status_code)
            status_code = res.status_code
            if res.text:
                response = json.loads(res.text)
        except Exception as error_msg:
            request_time_out_status = True
            self.get_error_info(error_msg)

        return request_time_out_status, response, status_code

# |----------------------End of send_request_to_host--------------------------|

# |----------------------------------------------------------------------------|
# prepare_request_params
# |----------------------------------------------------------------------------|
    def prepare_request_params(self, scanner_ip, request_name,
                               data, params, time_out, port,
                               request_type, headers=None):
        if port is None:
            url = "https://{}/{}".format(scanner_ip, request_name)
        else:
            url = "http://{}:{}/{}".format(scanner_ip, port, request_name)
        request_json = {
                "url": url,
                "time_out": time_out,
                "params": params,
                "data": data,
                "headers": headers,
                "request_type": request_type
            }
        return request_json

# |----------------------End of prepare_request_params------------------------|

# |----------------------------------------------------------------------------|
# is_app_alive
# |----------------------------------------------------------------------------|
    def is_app_alive(self, host):
        params = {}
        data = {}

        # Get wsi_backend port from config file.
        wsi_port = self.get_wsi_backend_port()
        time_out = 10
        request_json = self.prepare_request_params(host, "scanner/is_alive",
                                                   data, params, time_out,
                                                   wsi_port, "GET")
        request_time_out_status, response, status_code =\
            self.send_request_to_host(request_json)

        return request_time_out_status, response

# |----------------------End of is_app_alive----------------------------------|

# # |----------------------------------------------------------------------------|
# # ping_host
# # |----------------------------------------------------------------------------|
    def ping_host(self, host):
        try:
            # Building the command. Ex: "ping -c 1 google.com"
            param = '-n' if platform.system().lower()=='windows' else '-c'
            command = ['ping', param, '1', host]
            res = subprocess.call(command) == 0
            return res
        except Exception:
            return False

# |---------------------------End of ping_host-----------------------------------|
