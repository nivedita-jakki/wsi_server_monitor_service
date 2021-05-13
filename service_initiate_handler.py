import subprocess
import time
from os.path import join

from utilities import Utilities
from config_reader import ConfigReader

# ==============================================================================
# ServiceInitiateHandler
# ==============================================================================
class ServiceInitiateHandler():

# |----------------------------------------------------------------------------|
# __init__
# |----------------------------------------------------------------------------|
    def __init__(self):
        self._config_reader_interface = ConfigReader()
        self._utility_obj = Utilities()
        self._startup_path = self._utility_obj.get_scripts_path()

# |----------------------End of __init__--------------------------------------|

# |----------------------------------------------------------------------------|
# get_system_ip
# |----------------------------------------------------------------------------|
    def get_system_ip(self):
        proce_resp = subprocess.check_output(['hostname', '-I'])
        proce_resp_str = proce_resp.decode('utf-8')
        proce_resp_str_list = proce_resp_str.split()
        print("proce_resp_str_list:", proce_resp_str_list)
                
        return proce_resp_str_list

# |----------------------End of get_system_ip---------------------------------|

# |----------------------------------------------------------------------------|
# start_services
# |----------------------------------------------------------------------------|
    def start_services(self):
        self._utility_obj.change_directory(self._startup_path)
        service_type = self._config_reader_interface.\
                        get_monitor_service_type()
        
        if service_type == "cluster":
            # Run arm emulated mode script
            emulated_mode_status = self._config_reader_interface.\
                    get_emulated_mode()
            
            if emulated_mode_status is True:
                self._run_arm_server()

            # Initiate django
            self._start_cluster_django()
            # Initiate celery
            self._start_cluster_celery()
            # Initiate viewer frontend
            self._start_viewer_frontend_server()
            # Initiate viewer backend
            self._start_viewer_backend_server()
            # Initiate transfer service
            self._start_transfer_service()
            # Initiate monitoring service
            self._start_data_monitoring_service()
            # Initiate cluster
            self._start_cluster()
            # Initiate scan_performance_service
            self._start_scan_performance()
            # Initiate filebeat
            self._start_file_beat()
            # Open Chrome
            self._open_chrome()
        elif service_type == "scanner":
            # Run capture test
            self._run_capture_test()
            # Initiate scanner service
            self._start_scanner_service()
            # Initiate django
            self._start_scanner_django()
            # Initiate celery
            self._start_scanner_celery()
            # Initiate transfer service
            self._start_transfer_service()
            # Initiate filebeat
            self._start_file_beat()
            # Initiate scanner
            self._start_scanner()
        else:
            # Initiate viewer frontend
            self._start_viewer_frontend_server()
            # Initiate viewer backend
            self._start_viewer_backend_server()
            # Initiate panorama viewer
            self._start_panorama_server()
            # Initiate transfer service
            self._start_data_monitoring_service()
            # Initiate indexing service
            self._start_data_indexing_service()
            # Initiate restoration service_1
            self._start_restoration_service()
            # Initiate restoration service_2
            self._start_restoration_service_2()
            # Initiate image format service
            self._start_image_format_service()
            # Initiate registration service
            self._start_registration_service()
            # Initiate filebeat
            self._start_file_beat()
            # Initiate scan_performance_service
            self._start_scan_performance()
            # Open Chrome
            self._open_chrome()

        self._utility_obj.\
            change_directory(join(self._utility_obj.get_home_path(),
                                    "wsi_server_monitor_service"))
        return True

# |----------------------End of start_services-------------------------------|

# |----------------------------------------------------------------------------|
# _start_transfer_service
# |----------------------------------------------------------------------------|
    def _start_transfer_service(self):
        subprocess.Popen(["./data_transfer_service.sh"], shell=True)

# |----------------------End of _start_transfer_service-----------------------|

# |----------------------------------------------------------------------------|
# _start_viewer_frontend_server
# |----------------------------------------------------------------------------|
    def _start_viewer_frontend_server(self):
        status = False
        # Get front end port from config file.
        port = self._config_reader_interface.get_viewer_front_end_port()

        status = self._utility_obj.is_port_exists(port)
        counter = 1

        subprocess.Popen(["./frontend_server.sh"], shell=True)

        while status is False and counter <= 120:
            print("Counter: {}".format(counter))
            status = self._utility_obj.is_port_exists(port)
            time.sleep(1)
            counter = counter + 1

        return status
    
# |----------------------End of _start_viewer_frontend_server-----------------|

# |----------------------------------------------------------------------------|
# _start_viewer_backend_server
# |----------------------------------------------------------------------------|
    def _start_viewer_backend_server(self):
        status = False
        # Get back end port from config file.
        port = self._config_reader_interface.get_viewer_back_end_port()

        status = self._utility_obj.is_port_exists(port)
        counter = 1

        subprocess.Popen(["./node_server.sh"], shell=True)

        while status is False and counter <= 120:
            print("Counter: {}".format(counter))
            status = self._utility_obj.is_port_exists(port)
            time.sleep(1)
            counter = counter + 1

        return status
    
# |----------------------End of _start_viewer_backend_server------------------|

# |----------------------------------------------------------------------------|
# _start_panorama_server
# |----------------------------------------------------------------------------|
    def _start_panorama_server(self):
        status = False
        # Get panorama port from config file.
        port = self._config_reader_interface.get_panorama_viewer_port()
        status = self._utility_obj.is_port_exists(port)

        counter = 1

        subprocess.Popen(["./panorama_server.sh"], shell=True)

        while status is False and counter <= 120:
            print("Counter: {}".format(counter))
            status = self._utility_obj.is_port_exists(port)
            time.sleep(1)
            counter = counter + 1

        return status

# |----------------------End of _start_panorama_server------------------------|

# |----------------------------------------------------------------------------|
# _start_encoding_service
# |----------------------------------------------------------------------------|
    def _start_encoding_service(self):
        subprocess.Popen(["./encoding_service.sh"], shell=True)

# |----------------------End of _start_encoding_service-----------------------|

# |----------------------------------------------------------------------------|
# _start_file_beat
# |----------------------------------------------------------------------------|
    def _start_file_beat(self):
        subprocess.Popen(["./file_beat.sh"], shell=True,
                        stdout=subprocess.PIPE)
# |----------------------End of _start_file_beat------------------------------|

# |----------------------------------------------------------------------------|
# _open_chrome
# |----------------------------------------------------------------------------|
    def _open_chrome(self):
        subprocess.Popen(["./open_chrome.sh"], shell=True,
                        stdout=subprocess.PIPE)

# |----------------------End of _open_chrome----------------------------------|

# |----------------------------------------------------------------------------|
# _start_data_monitoring_service
# |----------------------------------------------------------------------------|
    def _start_data_monitoring_service(self):
        subprocess.Popen(["./data_monitoring_service.sh"], shell=True,
                        stdout=subprocess.PIPE)

# |----------------------End of _start_data_monitoring_service----------------|

# |----------------------------------------------------------------------------|
# _start_data_indexing_service
# |----------------------------------------------------------------------------|
    def _start_data_indexing_service(self):
        subprocess.Popen(["./data_indexing_service.sh"], shell=True,
                        stdout=subprocess.PIPE)

# |----------------------End of _start_data_indexing_service------------------|

# |----------------------------------------------------------------------------|
# _start_restoration_service
# |----------------------------------------------------------------------------|
    def _start_restoration_service(self):
        subprocess.Popen(["./restoration_service_1.sh"], shell=True,
                        stdout=subprocess.PIPE)

# |----------------------End of _start_restoration_service--------------------|

# |----------------------------------------------------------------------------|
# _start_restoration_service_2
# |----------------------------------------------------------------------------|
    def _start_restoration_service_2(self):
        subprocess.Popen(["./restoration_service_2.sh"], shell=True,
                         stdout=subprocess.PIPE)

# |---------------------End of _start_restoration_service_2-------------------|

# |----------------------------------------------------------------------------|
# _start_image_format_service
# |----------------------------------------------------------------------------|
    def _start_image_format_service(self):
        subprocess.Popen(["./wsi_image_format_service.sh"], shell=True,
                         stdout=subprocess.PIPE)

# |----------------------End of _start_image_format_service--------------------|

# |----------------------------------------------------------------------------|
# _start_registration_service
# |----------------------------------------------------------------------------|
    def _start_registration_service(self):
        subprocess.Popen(["./registartion_rotation_scalling_service.sh"],
                         shell=True, stdout=subprocess.PIPE)

# |----------------------End of _start_registration_service--------------------|

# |----------------------------------------------------------------------------|
# _start_cluster_django
# |----------------------------------------------------------------------------|
    def _start_cluster_django(self):
        subprocess.Popen(["./cluster_server.sh"], shell=True)

# |----------------------End of _start_cluster_django-------------------------|

# |----------------------------------------------------------------------------|
# _start_scanner_django
# |----------------------------------------------------------------------------|
    def _start_scanner_django(self):
        subprocess.Popen(["./scanner_server.sh"], shell=True)
        
        status = False
        
        scanner_django_port = self._config_reader_interface.\
                                get_scanner_django_port()
        counter = 0
        
        while status is False and counter <= 120:
            print("Counter: {}".format(counter))
            status = self._utility_obj.is_port_exists(scanner_django_port)
            time.sleep(1)
            counter = counter + 1

# |----------------------End of _start_scanner_django-------------------------|

# |----------------------------------------------------------------------------|
# _start_scanner_service
# |----------------------------------------------------------------------------|
    def _start_scanner_service(self):
        subprocess.Popen(["./scanner_service.sh"], shell=True)
        
        status = False
        
        scanner_service_port = self._config_reader_interface.\
                                get_scanner_service_port()
        counter = 0
        
        while status is False and counter <= 120:
            print("Counter: {}".format(counter))
            status = self._utility_obj.is_port_exists(scanner_service_port)
            time.sleep(1)
            counter = counter + 1
            
# |----------------------End of _start_scanner_service------------------------|

# |----------------------------------------------------------------------------|
# _start_cluster_celery
# |----------------------------------------------------------------------------|
    def _start_cluster_celery(self):
        subprocess.Popen(["./cluster_celery.sh"], shell=True)

# |----------------------End of _start_cluster_celery-------------------------|

# |----------------------------------------------------------------------------|
# _start_scanner_celery
# |----------------------------------------------------------------------------|
    def _start_scanner_celery(self):
        subprocess.Popen(["./scanner_celery.sh"], shell=True)

# |----------------------End of _start_scanner_celery-------------------------|

# |----------------------------------------------------------------------------|
# _start_scanner
# |----------------------------------------------------------------------------|
    def _start_scanner(self):
        subprocess.Popen(["./start_scanner"], shell=True,
                        stdout=subprocess.PIPE)
# |----------------------End of _start_scanner--------------------------------|

# |----------------------------------------------------------------------------|
# _start_cluster
# |----------------------------------------------------------------------------|
    def _start_cluster(self):
        subprocess.Popen(["./start_cluster"], shell=True,
                        stdout=subprocess.PIPE)

# |----------------------End of _start_cluster--------------------------------|

# |----------------------------------------------------------------------------|
# _run_capture_test
# |----------------------------------------------------------------------------|
    def _run_capture_test(self):
        subprocess.Popen(["./capture_test"], shell=True)

# |----------------------End of _run_capture_test-----------------------------|

# |----------------------------------------------------------------------------|
# _run_arm_server
# |----------------------------------------------------------------------------|
    def _run_arm_server(self):
        subprocess.Popen(["./emulator_arm.sh"], shell=True)

# |----------------------End of _run_arm_server-------------------------------|

# |----------------------------------------------------------------------------|
# _start_scan_performance
# |----------------------------------------------------------------------------|
    def _start_scan_performance(self):
        subprocess.Popen(["./scan_performance_service.sh"], shell=True)

# |------------------End of _start_scan_performance---------------------------|
