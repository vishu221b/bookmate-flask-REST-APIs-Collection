import datetime


def convert_time(time: str):
    time = str(datetime.datetime.strptime(time, "%Y-%m-%d"))
    return time
