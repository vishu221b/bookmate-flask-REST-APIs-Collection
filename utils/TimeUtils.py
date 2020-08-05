import datetime


class TimeUtils:
    def __init__(self):
        pass

    def calculate_difference_from_now(self, timestamp):
        now = round(datetime.datetime.now().timestamp()*1000000)
        return timestamp-now

    def format_epoch_to_date_time(self, timestamp):
        return datetime.datetime.fromtimestamp(timestamp)


def convert_time(time: str):
    time = str(datetime.datetime.strptime(time, "%Y-%m-%d"))
    return time
