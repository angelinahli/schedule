
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

def run():
    ws = client.open_by_url(usr.SHEETURL).worksheet(usr.SHEETNAME)

    today_hours = float(raw_input(
        "How much time do you have today? (in hours) ").strip())

    today_schedule = Schedule(today_hours, tasks=get_tasks(ws))
    print(today_schedule.format_schedule())
    print(today_schedule.format_future_todos())

if __name__ == "__main__":
    run()