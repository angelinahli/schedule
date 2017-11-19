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

def get_valid_hours():
    try:
        return float(raw_input(
            "How much time do you have today (in hours)? ").strip())
    except ValueError:
        print("Sorry, this input is invalid - please try again.\n")
        return get_valid_hours()

def get_valid_mode():
    try:
        mode = int(raw_input(
                "Do you want any tasks (1), short tasks (2) or long tasks (3)? "
            ).strip())
        
        if mode not in range(1, 4):
            print("Please enter a number between 1 and 3.\n")
            return get_valid_mode()

        return mode
    except ValueError:
        print("Sorry, this input is invalid - please try again.\n")
        return get_valid_mode()

def run():
    ws = client.open_by_url(usr.SHEETURL).worksheet(usr.SHEETNAME)
    hours = get_valid_hours()
    mode = get_valid_mode()

    today_schedule = Schedule(hours=hours, mode=mode, tasks=get_tasks(ws))
    today_schedule.print_all()

if __name__ == "__main__":
    run()
