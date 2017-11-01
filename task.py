"""
FILENAME: task.py
DESCR: Represents a Task that should be completed and its properties
AUTHOR: Angelina Li
DATE: 10/30/2017
"""
from datetime import datetime, date

class Task(object):
    """
    Task that needs to be completed. Has the following properties:

    Attributes:
        description: String representing task description
        time: int representing how many hours task will take to complete
        weight: int representing importance of task in cardinal rating from 0-5
        due: datetime representing time this task is due
        complete: boolean representing whether the task is done
    """

    def __init__(self, description, time, weight, due):
        """Return a Task object with the attributes as described above.
            due will be represented as a string.
        """
        self.description = description
        self.time = float(time)
        self.weight = float(weight)
        self.due = datetime.strptime(due, "%Y-%m-%d")

        self.weight_per_hr = self.weight / self.time
        self.due_by_tomorrow = self._is_due_by_tomorrow()

    def _convert_vals(self, fn, val, default):
        try:
            return fn(val)
        except ValueError:
            return default

    def _is_due_by_tomorrow(self):
        """returns whether the task is due by tomorrow or overdue.
        """
        today = datetime.today()
        due_soon = (today > self.due) or (self.due - today).days < 1.75
        return 1 if due_soon else 0

    def __repr__(self):
        return ("\nTask: {desc} \n\ttime: {time} \n\tweight: {wgt} \n\tdue: {due} " + 
            "\n\twgt_p_hr: {wph} \n\tdue_by_tmrw: {dbt}").format(
            desc=self.description,
            time=self.time,
            wgt=self.weight,
            due=self.due,
            wph=self.weight_per_hr,
            dbt=self.due_by_tomorrow)