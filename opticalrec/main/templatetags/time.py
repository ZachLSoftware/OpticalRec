from django import template

register = template.Library()
@register.filter
def get_time(timestamp):
    minutes=int(timestamp/60)
    seconds=int(round((timestamp/60 %1)*60))
    if seconds < 10:
        seconds="0" + str(seconds)
    else:
        seconds=str(seconds)
    time=str(minutes)+":"+seconds

    return time