from jdatetime import datetime as jdatetime, datetime

JALALI_MONTHS = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
                 "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
WEEKDAYS_SHORT = ["د", "س", "چ", "پ", "ج", "ش", "ی"]            # date.weekday(): Monday = 0
WEEKDAYS = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه", "شنبه", "یکشنبه"]

def jnow() -> datetime:
    return jdatetime.now()

def jtoday() -> datetime:
    return jdatetime.today()

