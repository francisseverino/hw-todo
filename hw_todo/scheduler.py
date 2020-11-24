from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from .utils import get_canvas_tasks
import atexit

# initialize scheduler
scheduler = BackgroundScheduler(timezone=utc)
# Add Job to the scheduler
scheduler.add_job(func=get_canvas_tasks, trigger="interval", hours=24)
# Start Scheduler
scheduler.start()
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
