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
