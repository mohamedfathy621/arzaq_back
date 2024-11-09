from django.utils import timezone

def dates():
    now = timezone.now()
    start_of_year = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start_of_week = now - timezone.timedelta(days=now.weekday())
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return {'start_of_year':start_of_year,'start_of_month':start_of_month,'start_of_week':start_of_week,'start_of_day':start_of_day}