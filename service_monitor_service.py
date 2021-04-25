import requests
import time
from fastapi import FastAPI, Request, BackgroundTasks
from config_reader import ConfigReader
from service_initiate_handler import ServiceInitiateHandler

service_monitor_app = FastAPI()
config_reader_interface = ConfigReader()

# |----------------------------------------------------------------------------|
# initiate_service
# |----------------------------------------------------------------------------|
@service_monitor_app.post("/start_service")
def initiate_service(self):
    service_type = config_reader_interface.get_monitor_service_type()
    service_initiate_handler = ServiceInitiateHandler(service_type) 

    ip_list = []
    
    counter = 120
    
    while len(ip_list) < 0 and counter < 120:
        ip_list = service_initiate_handler.get_system_ip()
        counter = counter + 1
        time.sleep(2)
    
    if len(ip_list) > 0:
        service_initiate_handler.start_services()

    return {"success": True}

# |------------------------End of initiate_service----------------------------|