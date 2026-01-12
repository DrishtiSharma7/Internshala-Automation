# bot/report_simple.py

import csv
import os
from time import strftime, localtime

LOG_FILE = "applications_log.csv"

def log_application(profile, company, link, status, reason=""):
    file_exists = os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Date", "Profile", "Company", "Link", "Status", "Reason"])
        writer.writerow([
            strftime("%d-%b-%Y", localtime()),
            profile,
            company,
            link,
            status,
            reason,
        ])
