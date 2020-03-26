import os
import sqlite3

current_path = os.path.dirname(os.path.abspath(__file__))


def init_con_cur():
    connection = sqlite3.connect(current_path+'/../store/BMS.db', check_same_thread=True)
    cursor = connection.cursor()
    return [connection, cursor]
