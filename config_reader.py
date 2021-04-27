import os
from os.path import join
from lxml import etree

# ==============================================================================
# ConfigReader
# ==============================================================================

class ConfigReader():

# |----------------------------------------------------------------------------|
# __init__
# |----------------------------------------------------------------------------|
    def __init__(self):
        self.config_path = join(os.getcwd(), "config",
                                "server_monitor_config.xml")     
        
# |----------------------End of __init__--------------------------------------|

# |----------------------------------------------------------------------------|
# get_root
# |----------------------------------------------------------------------------|
    def get_root(self):
        xml_file = etree.parse(self.config_path)
        root_tag = xml_file.getroot()
        return root_tag

# |----------------------End of get_root--------------------------------------|

# |----------------------------------------------------------------------------|
# get_sub_tag
# |----------------------------------------------------------------------------|
    def get_sub_tag(self, root_tag, name):
        return root_tag.find(name)

# |----------------------End of get_sub_tag-----------------------------------|

# |----------------------------------------------------------------------------|
# get_value_by_name
# |----------------------------------------------------------------------------|
    def get_value_by_name(self, root_tag, name):
        value = None

        try:
            sub_tag = self.get_sub_tag(root_tag, name)
            if sub_tag is not None:
                value = sub_tag.attrib["value"]
        except Exception as error_msg:
            print("error_msg in get_value_by_name: ", error_msg)
        return value

# |----------------------End of get_value_by_name-----------------------------|

# |----------------------------------------------------------------------------|
# get_monitor_service_type
# |----------------------------------------------------------------------------|
    def get_monitor_service_type(self):
        root_tag = self.get_root()
        monitor_service_type = self.get_value_by_name(root_tag,
                                                      "monitor_service_type")
        return monitor_service_type

# |----------------------End of get_monitor_service_type----------------------|

# |----------------------------------------------------------------------------|
# get_viewer_front_end_port
# |----------------------------------------------------------------------------|
    def get_viewer_front_end_port(self):
        front_end_port = None

        try:
            root_tag = self.get_root()
            sub_tag = self.get_sub_tag(root_tag, "port")
            sub_tag = self.get_sub_tag(sub_tag, "cluster")
            front_end_port = self.get_value_by_name(sub_tag,
                                                    "viewer_front_end")
        except Exception as error_msg:
            print("error_msg in  get_viewer_front_end_port: ", error_msg)
    
        return front_end_port
    
# |----------------------End of get_viewer_front_end_port---------------------|

# |----------------------------------------------------------------------------|
# get_viewer_back_end_port
# |----------------------------------------------------------------------------|
    def get_viewer_back_end_port(self):
        back_end_port = None

        try:
            root_tag = self.get_root()
            sub_tag = self.get_sub_tag(root_tag, "port")
            sub_tag = self.get_sub_tag(sub_tag, "cluster")
            back_end_port = self.get_value_by_name(sub_tag,
                                                   "viewer_back_end")
        except Exception as error_msg:
            print("error_msg in  get_viewer_back_end_port: ", error_msg)
    
        return back_end_port

# |----------------------End of get_viewer_back_end_port----------------------|

# |----------------------------------------------------------------------------|
# get_panorama_viewer_port
# |----------------------------------------------------------------------------|
    def get_panorama_viewer_port(self):
        panorama_viewer_port = None

        try:
            root_tag = self.get_root()
            sub_tag = self.get_sub_tag(root_tag, "port")
            sub_tag = self.get_sub_tag(sub_tag, "cluster")
            panorama_viewer_port = self.get_value_by_name(sub_tag,
                                                          "panorama_viewer")
        except Exception as error_msg:
            print("error_msg in  get_panorama_viewer_port: ", error_msg)
    
        return panorama_viewer_port
    
# |----------------------End of get_panorama_viewer_port-----------------------|

# |----------------------------------------------------------------------------|
# get_robotic_arm_ip
# |----------------------------------------------------------------------------|
    def get_robotic_arm_ip(self):
        root_tag = self.get_root()
        robotic_arm_ip = self.get_value_by_name(root_tag, "robotic_arm_ip")
        return robotic_arm_ip

# |----------------------End of get_robotic_arm_ip----------------------------|
