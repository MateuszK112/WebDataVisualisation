import threading
from api_request import get_url_data
from project_db import *
import time as tm


class Get_Data(threading.Thread):
    def run(self):
        global stop_getting_data
        stop_getting_data = False
        while stop_getting_data == False:
            add_data_record("1", get_url_data("1"))
            add_data_record("2", get_url_data("2"))
            add_data_record("3", get_url_data("3"))
            add_data_record("4", get_url_data("4"))
            add_data_record("5", get_url_data("5"))
            add_data_record("6", get_url_data("6"))
            data_expiration(600)
            tm.sleep(1)
