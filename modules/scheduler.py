from threading import Timer
from datetime import datetime


def create_job(string_date: str, task):
    """Create new job for a task.

    Parameters
    ----------
    string_date : str
        format `%d/%m/%Y %H:%M:%S.%f`
    task : func
        Task needed to schedule
    """
    format_data = "%d/%m/%Y %H:%M:%S.%f"
    run_at = datetime.strptime(string_date, format_data)
    now = datetime.now()
    delay = (run_at - now).total_seconds()
    return Timer(delay, task)
