"""
FILENAME: task.py
DESCR: Represents a Task that should be completed and its properties
AUTHOR: Angelina Li
DATE: 10/30/2017
"""
from datetime import datetime

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
        self.urgency = self._get_urgency()

        self.quad = None

    def _get_urgency(self):
        """
        Returns the normalized difference in the number of days between today
        and the event due day. (Tasks due sooner have a higher urgency)
        
        Normalized difference: number of days between today and the due date
        + 3, such that tasks due tomorrow have a normalized difference of 1.
        """
        today = datetime.today().date()
        due_date = self.due.date()
        diff = (today - due_date).days

        return diff + 3

    def __repr__(self):
        return ("\nTask: {desc} \n\ttime: {time} \n\tweight: {wgt} " + 
            "\n\tdue: {due} \n\twgt_p_hr: {wph} \n\turgency: {urg} " +
            "\n\tquadrant: {quad}").format(
                desc=self.description,
                time=self.time,
                wgt=self.weight,
                due=self.due,
                wph=self.weight_per_hr,
                urg=self.urgency,
                quad=self.quad
                )
