import time
from fastapi import FastAPI, BackgroundTasks
from service_initiate_handler import ServiceInitiateHandler

service_monitor_app = FastAPI()

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
        service_initiate_handler.start_services()
    
# |------------------------End of initiate_service----------------------------|