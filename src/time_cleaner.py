import math
from datetime import datetime

def getTime(time_str):
    datetime_object = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    time = now - datetime_object
   
    if time.days > 365:
        years = math.floor(time.days/365)
        if years == 1:
            return str(years) + " year ago"
        return str(years) + " years ago"
    elif time.days > 30:
        months = math.floor(time.days/30)
        if months == 1:
            return str(months) + " month ago"
        return str(months) + " months ago"
    elif time.days > 7:
        weeks = math.floor(time.days/7)
        if weeks == 1:
            return str(weeks) + " week ago"
        return str(weeks) + " weeks ago"
    elif time.days < 1: 
        hour = int(time.seconds / 3600)
        if hour > 1:
            return str(hour) + " hours ago"
        if hour == 1: 
            return str(hour) + " hour ago"
        if hour < 1:
            minute = int(time.seconds / 60)
            if minute < 1:
                return "just now"
            if minute == 1:
                return str(minute) + " minute ago"
            return str(minute) + " minutes ago"
    elif time.days == 1:
        return str(time.days) + " day ago"
    else: 
        return str(time.days) + " days ago"