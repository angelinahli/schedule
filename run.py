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
    msg = ["\nDATE: {}\n\nTO DO:".format(date.today())]
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

def run():
    today_hours = float(raw_input(
        "How much time do you have today? (in hours) ").strip())

    ws = client.open_by_url(usr.SHEETURL).worksheet(usr.SHEETNAME)
    today_schedule = Schedule(today_hours, tasks=get_tasks(ws))
    print(format_schedule(today_schedule))

if __name__ == "__main__":
    run()