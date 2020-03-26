import datetime


def convert_time(time:str):
    time = str(datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.000Z"))
    return time
