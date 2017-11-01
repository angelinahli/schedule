"""
FILENAME: schedule.py
DESCR: Represents a Schedule that tells user what to complete and in
what order
AUTHOR: Angelina Li
DATE: 10/30/17
"""

from task import Task

class Schedule(object):
    """
    Schedule that remembers all of the tasks I have yet to do (while running)
    and lists the things I need to do in order.
    """

    def __init__(self, hours, tasks=[]):
        self.hours = hours
        self.tasks = tasks

    def _sort(self):
        """
        Sort the tasks by importance per unit time.
        """
        self.tasks.sort(
            key=lambda task: (task.due_by_tomorrow, task.weight_per_hr), 
            reverse=True)

    def get_scheduled_tasks(self):
        self._sort()

        todo = []
        total_time = 0

        for task in self.tasks:
            
            total_time += task.time
            todo.append(task)

            if total_time >= self.hours:
                break

        return todo