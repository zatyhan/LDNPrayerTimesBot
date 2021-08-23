from flask import Flask
import times

import atexit
from apscheduler.schedulers.background import BackgroundScheduler


def job():
    times.tweet()
    print("Success")


scheduler = BackgroundScheduler()
scheduler.add_job(func=job, trigger="interval", seconds=60)
scheduler.start()

application = Flask(__name__)


@application.route("/")
def index():
    return "Follow @LDNPrayerTimes!"


atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    application.run(port=5000, debug=True)