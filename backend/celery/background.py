import time
from base import app


@app.task
def generate_report_task(arg1, arg2):
    print("Start generating report")
    time.sleep(10)
    print("Report generated")
