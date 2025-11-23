# utils/scheduler.py
import schedule
import time

def run_every(hours, func):
    schedule.every(hours).hours.do(func)

    while True:
        schedule.run_pending()
        time.sleep(1)
