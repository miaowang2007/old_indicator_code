from datetime import datetime


def date2str(date, format):
    return date.strftime(format)


def str2date(my_str):
    return datetime.strptime(my_str, "%Y-%m-%d")