import datetime
today = datetime.date.today()
first = today.replace(day=1)
lastday = first - datetime.timedelta(days=1)
firstday = first - datetime.timedelta(days=31)
print lastday.strftime("%Y-%m-%d")
print firstday.strftime("%Y-%m-%d")
