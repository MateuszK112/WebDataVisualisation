import sqlite3
import time as tm


def make_database():
    connection = sqlite3.connect('feet-pressure.db')
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS data (
    timestamp integer,
    patient_id nvarchar,
    value1 integer,
    value2 integer,
    value3 integer,
    value4 integer,
    value5 integer,
    value6 integer,
    anomaly1 nvarchar,
    anomaly2 nvarchar,
    anomaly3 nvarchar,
    anomaly4 nvarchar,
    anomaly5 nvarchar,
    anomaly6 nvarchar,
    time_fetched time )""")
    connection.commit()
    cursor.close()
    connection.close()


def delete_data():
    connection = sqlite3.connect('feet-pressure.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM data")
    connection.commit()
    cursor.close()
    connection.close()


def data_expiration(time_ago_sec):
    connection = sqlite3.connect('feet-pressure.db')
    cursor = connection.cursor()
    time_check = tm.time()
    cursor.execute("""DELETE FROM data WHERE (?) - timestamp > (?) """, (time_check, time_ago_sec))
    connection.commit()


def get_all_data():
    connection = sqlite3.connect('feet-pressure.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM data """)
    data = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return data


def get_anomaly_data():
    connection = sqlite3.connect('feet-pressure.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT patient_id, value1, value2, value3, value4, value5, value6 from data where anomaly1='1'""")
    data = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return data


def add_data_record(pid, data_record):
    connection = sqlite3.connect('feet-pressure.db')
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO data (timestamp, patient_id, value1, value2, value3, value4, value5, value6,
                      anomaly1, anomaly2, anomaly3, anomaly4, anomaly5, anomaly6, time_fetched) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                   (data_record["timestamps"], pid, data_record["values"][0],
                    data_record["values"][1], data_record["values"][2], data_record["values"][3],
                    data_record["values"][4], data_record["values"][5],
                    data_record["anomalies"][0], data_record["anomalies"][1], data_record["anomalies"][2],
                    data_record["anomalies"][3],
                    data_record["anomalies"][4], data_record["anomalies"][5], tm.time()))
    connection.commit()
