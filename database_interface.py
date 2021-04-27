import psycopg2

from utilities import Utilities

# ==============================================================================
# DatabaseInterface
# ==============================================================================


class DatabaseInterface():
    '''
    Interface class to talk to the PostgreSQL database
    '''
# |----------------------------------------------------------------------------|
# Class Variables
# |----------------------------------------------------------------------------|
#        no class variables

# |----------------------------------------------------------------------------|
# Constructor
# |----------------------------------------------------------------------------|
    def __init__(self):
        self._utility_obj = Utilities()
        self._db_conn = None

# |---------------------------End of Constructor------------------------------|

# |----------------------------------------------------------------------------|
# _connect_to_db
# |----------------------------------------------------------------------------|
    def _connect_to_db(self):
        db_json_path = self._utility_obj.get_db_credential_path()

        db_conn_dict = self._utility_obj.read_json(db_json_path)

        self._db_conn = psycopg2.connect(**db_conn_dict)
        
# |---------------------------End of _connect_to_db---------------------------|

# |----------------------------------------------------------------------------|
# get_scanner_info
# |----------------------------------------------------------------------------|
    def get_scanner_info(self):
        scanner_list = []

        try:
            cursor = self._db_conn.cursor()
            query = ("SELECT scanner_ip, machine_serial_number, "
                     "scanner_position, FROM cluster.scanner_info")

            print(query)
            cursor.execute(query)
            data = cursor.fetchall()[0]

            for scanner in data:
                scanner_obj = {
                        "scanner_ip": scanner[0],
                        "scanner_name": scanner[1],
                        "scanner_position": scanner[2]
                    }
                scanner_list.append(scanner_obj)

            cursor.close()
        except psycopg2.DatabaseError as error:
            print("error in getting scanner info: ", error)

        return scanner_list

# |------------------------End of get_scanner_info----------------------------|
