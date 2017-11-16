"""
FILENAME: schedule.py
DESCR: Represents a Schedule that tells user what to complete and in
what order
AUTHOR: Angelina Li
DATE: 10/30/17
"""
from datetime import date

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
            key=lambda task: (task.due_by_tomorrow, task.weight_per_hr, task.due), 
            reverse=True)

    def get_tasks_per_day(self):
        """
        Will return a dictionary mapping each date onto the total hours of
        work due on that date, as well as a list of all the tasks due
        on that date.

        return_dct = {
            datetime: {
                "hours": num_hours, 
                "tasks": [list of Task() objs due on this date]
            }
        }
        """
        dates = {}
        for task in self.tasks:
            date_dct = dates.get(
                task.due, {
                    "hours": 0, 
                    "tasks": []}
                )
            date_dct["hours"] += task.time
            date_dct["tasks"].append(task)
            dates[task.due] = date_dct
        return dates

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

    def format_schedule(self):
        msg = ["\nDATE: {}\n\n\nTO DO:".format(date.today())]
        tasks = self.get_scheduled_tasks()
        for i, task in enumerate(tasks):
            task_msg = ("{num}. {desc} \n\t- est. time: {time} hours " + 
                "\n\t- bang 4 buck: ${wgt}/hr\n\t- due: {due}").format(
                num=i + 1,
                desc=task.description,
                wgt=round(task.weight_per_hr, 2),
                time=task.time,
                due=task.due.strftime("%a %b %d"))
            msg.append(task_msg)
        return "\n\n".join(msg)

    def format_future_todos(self):
        msg = ["\n\nWORK DUE IN UPCOMING DAYS:"]
        dates = sorted(self.get_tasks_per_day().items(), key=lambda tup: tup[0])
        for date, date_dct in dates:
            date_msg = [
                "* {date} - {hrs} HOURS".format(
                    date=date.strftime("%a %b %d"),
                    hrs=date_dct["hours"])
            ]
            
            date_tasks = sorted(date_dct["tasks"], 
                key=lambda task: task.weight_per_hr, 
                reverse=True)
            
            for task in date_tasks:
                date_msg.append(
                    "\t* ({time} hrs) {desc} - ${wgt}/hr".format(
                        desc=task.description,
                        time=task.time,
                        wgt=round(task.weight_per_hr, 2))
                )
            msg.append("\n".join(date_msg))
        return "\n\n".join(msg)