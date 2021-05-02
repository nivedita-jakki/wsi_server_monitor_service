import time
import requests
from fastapi import FastAPI, BackgroundTasks
from fastapi_utils.tasks import repeat_every

from service_initiate_handler import ServiceInitiateHandler
from utilities import Utilities
from database_interface import DatabaseInterface
from config_reader import ConfigReader

service_monitor_app = FastAPI()
utility_obj = Utilities()
database_interface = DatabaseInterface()
config_interface = ConfigReader()


# |----------------------------------------------------------------------------|
# initiate_service
# |----------------------------------------------------------------------------|
@service_monitor_app.post("/start_service")
async def initiate_service(background_tasks: BackgroundTasks):
    background_tasks.add_task(service_initiator_task)
    
    return {"success": True}

# |------------------------End of initiate_service----------------------------|

# |----------------------------------------------------------------------------|
# service_initiator_task
# |----------------------------------------------------------------------------|
def service_initiator_task():
    service_initiate_handler = ServiceInitiateHandler() 
    
    ip_list = []
    counter = 1
    
    print("ip_list: ", ip_list)
    print("counter: ", counter)
    while len(ip_list) == 0 and counter < 120:
        print("counter in: ", counter)
        ip_list = service_initiate_handler.get_system_ip()
        counter = counter + 1
        print("Trying again.......")
        time.sleep(2)
    
    print("ip_list222: ", ip_list)
    if len(ip_list) > 0:
        status = service_initiate_handler.start_services()
        
#         if status is True:
#             health_check_url = "http://localhost:8024/startup"
#             resp = requests.post(url=health_check_url, timeout=5)
#             print(resp)

# |------------------------End of initiate_service----------------------------|

# |----------------------------------------------------------------------------|
# initiate_service
# |----------------------------------------------------------------------------|
@service_monitor_app.post("/startup") 
@repeat_every(wait_first=True,seconds=int(5))
def scheduled_task(background_tasks: BackgroundTasks) -> None:
    # Get scanner list
    scanner_info = database_interface.get_scann_info()
     
    # Append every scanner status into list.
    for scanner in scanner_info:
        # Get scanner online status
        request_time_out_status, response_json =\
            utility_obj.is_app_alive(scanner["scanner_ip"])
       
        if request_time_out_status is True:
            status = "offline"
            error_info = "Scanner server is down"
            background_tasks.add_task(status, error_info,
                                      scanner["scanner_name"],
                                      scanner["scanner_position"])
    
    # Create robotic arm status info json
    # get robotic_arm_ip from config file.
    robotic_arm_ip = config_interface.get_robotic_arm_ip()

    ret_val = utility_obj.ping_host(robotic_arm_ip)
    
    if ret_val is False:
        # Post UR3 as OFFLINE.
        pass
    
    return True

# |------------------------End of initiate_service----------------------------|

# |----------------------------------------------------------------------------|
# post_scanner_status
# |----------------------------------------------------------------------------|
    def post_scanner_status(self, scanner_status, error_info,
                            scanner_name, scanner_position):
        # Update scanner error.
        node_port = config_interface.get_viewer_back_end_port()
        cluster_host = "localhost"
        cluster_id = Utilities().get_cluster_name()
        request_name = "scanner/status"

        params = {}
        data = {
                "scanner_id": scanner_name,
                "cluster_id": cluster_id,
                "activity_status": scanner_status,
                "error_info": error_info,
                "position": scanner_position,
                "is_slide_found": False
            }

        Utilities().send_request_from_celery(request_name, cluster_host,
                                             node_port, params,
                                             data, "POST", time_out=None)

# |----------------------End of post_scanner_status---------------------------|
