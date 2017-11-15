from datetime import date

import config.user_info as usr
from config.gsheets import client
from schedule import Schedule
from task import Task

def get_task(data_dict):
    return Task(
        data_dict["description"], 
        data_dict["time"],
        data_dict["weight"],
        data_dict["due"])

def get_tasks(ws):
    """
    Given a worksheet, will return a list of tasks in that sheet
    """
    tasks = []
    for i in range(usr.STARTROW, ws.row_count + 1):
        row = ws.row_values(i)
        if not any(row):
            break
        
        data = {key: row[val - 1] for key, val in usr.cols.items()}
        if not data["complete"]:
            tasks.append(get_task(data))

    return tasks

def format_schedule(sch):
    """
    Given a Schedule object will format schedule nicely.
    """
    msg = ["\nDATE: {}\n\n\nTO DO:".format(date.today())]
    tasks = sch.get_scheduled_tasks()
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

def format_hours_per_day(sch):
    """
    Given a Schedule object will print out how many hours are associated
    with each day in the future
    """
    msg = ["\n\nWORK DUE IN UPCOMING DAYS:"]
    dates = sorted(sch.get_tasks_per_day().items(), key=lambda tup: tup[0])
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
                "\t- ({time} hrs) {desc} - ${wgt}/hr".format(
                    desc=task.description,
                    time=task.time,
                    wgt=round(task.weight_per_hr, 2))
            )
        msg.append("\n".join(date_msg))
    return "\n\n".join(msg)

def run():
    ws = client.open_by_url(usr.SHEETURL).worksheet(usr.SHEETNAME)

    today_hours = float(raw_input(
        "How much time do you have today? (in hours) ").strip())

    today_schedule = Schedule(today_hours, tasks=get_tasks(ws))
    print(format_schedule(today_schedule))
    print(format_hours_per_day(today_schedule))

if __name__ == "__main__":
    run()