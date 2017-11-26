"""
FILENAME: schedule.py
DESCR: Represents a Schedule that tells user what to complete and in
what order
AUTHOR: Angelina Li
DATE: 10/30/17
"""
from datetime import date
from numpy import median

from task import Task

class Schedule(object):
    """
    Schedule that remembers all of the tasks I have yet to do (while running)
    and lists the things I need to do in order.
    """
    MIN_WGT_PER_HR = 8

    def __init__(self, hours=0, mode=1, tasks=[]):
        self.hours = hours
        self.mode = mode
        self.tasks = tasks

    def _get_tasks_per_day(self):
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
            date_dct = dates.get(task.due, {"hours": 0, "tasks": []})
            
            date_dct["hours"] += task.time
            date_dct["tasks"].append(task)
            dates[task.due] = date_dct
        return dates

    def _get_quadrants(self):
        """
        Implements the Eisenhower matrix:
        - Tasks are urgent if due by tomorrow or sooner.
        - Tasks are important if their payout is at least $8/hr.
        Returns a list of tasks in order.
        """
        quadrants = {i: [] for i in range(1,5)}

        def add_quad(task, quad):
            task.quad = quad
            quadrants[quad].append(task)

        for task in self.tasks:
            if task.weight_per_hr >= self.MIN_WGT_PER_HR and task.urgency > 0:
                add_quad(task, 1)
            elif task.weight_per_hr >= self.MIN_WGT_PER_HR:
                add_quad(task, 2)
            elif task.urgency > 0:
                add_quad(task, 3)
            else:
                add_quad(task, 4)

        for i in quadrants:
            quadrants[i].sort(
                key=lambda task: (task.weight_per_hr, task.urgency),
                reverse=True)

        return quadrants

    def _format_todos(self):
        """
        Mode can either be:
        - 1 (do in order of Eisenhower matrix)
        - 2 (select short (<=45 min) tasks in order of Eisenhower matrix)
        - 3 (select long tasks in order of Eisenhower matrix)
        """
        quadrants = self._get_quadrants() # returns a dictionary
        tasks = []
        total_time = 0
        msg = ["\n\nTO DO:"]

        for i, task in enumerate(quadrants[1] + quadrants[2]):
            short = task.time < 1

            if self.mode == 1 or (self.mode == 2 and short) or (self.mode == 3
                    and not short):
                total_time += task.time
                tasks.append(task)
                msg.append("\n{}. ".format(i + 1) + task.get_msg())

            if total_time >= self.hours:
                break

        other_tasks = quadrants[3] + quadrants[4]
        if other_tasks:
            msg.append(("\n{}. Delegate or delete the following unimportant " + 
                "tasks: ").format(len(tasks) + 1))
            for task in other_tasks:
                short_msg = "\t- {desc} (quadrant {quad})".format(
                    desc=task.description,
                    quad=task.quad)
                msg.append(short_msg)

        return "\n".join(msg)

    def _format_future_todos(self):
        msg = ["\n\nWORK DUE IN UPCOMING DAYS:"]
        dates = sorted(self._get_tasks_per_day().items(), key=lambda tup: tup[0])
        
        for date, date_dct in dates:
            date_msg = [
                "* {date} - {hrs} HOURS".format(
                    date=date.strftime("%a %b %d"),
                    hrs=date_dct["hours"])
            ]
            
            date_tasks = sorted(date_dct["tasks"], 
                key=lambda task: (task.weight_per_hr, task.time),
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

    def print_all(self):
        print("\nDATE: {}".format(date.today()))
        print(self._format_todos())
        print(self._format_future_todos())

    def __repr__(self):
        msg = ["Schedule: {} hrs | {} mode | {} median wph".format(
            self.hours,
            self.mode,
            self.median_wph)]
        for task in self.tasks:
            msg.append(task.__repr__())
        return "\n".join(msg)