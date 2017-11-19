## Scheduling app
Small program that pulls information for a to-do list I have on my spreadsheet, and then prints out a curated to do list for the amount of time I have to work today.

Implements [Eisenhower's Matrix](http://www.eisenhower.me/eisenhower-matrix/), and optionally allows the user to complete only short or only long tasks if so desired.

### To add:
* Improve runtime
* Give user capability to update task immediately.

### Sample console output

```
user$ python run.py
How much time do you have today (in hours)? 10
Do you want any tasks (1), short tasks (2) or long tasks (3)? 1

DATE: 2017-11-18


TO DO:

1. Urgent important task 
    - est. time: 2.0 hours 
    - bang 4 buck: $25.0/hr
    -quadrant: 1
    - due: Sat Nov 18

2. Non urgent important task 
    - est. time: 3.0 hours 
    - bang 4 buck: $23.33/hr
    -quadrant: 2
    - due: Thu Nov 23

3. Delegate or delete the following unimportant tasks: 
    - Urgent non important task (quadrant 3)
    - Non urgent non important task (quadrant 4)


WORK DUE IN UPCOMING DAYS:

* Sat Nov 18 - 2.0 HOURS
    * (2.0 hrs) Urgent important task - $25.0/hr

* Sun Nov 19 - 3.0 HOURS
    * (3.0 hrs) Urgent non important task - $3.33/hr

* Thu Nov 23 - 3.0 HOURS
    * (3.0 hrs) Non urgent important task - $23.33/hr

* Fri Nov 24 - 2.0 HOURS
    * (2.0 hrs) Non urgent non important task - $6.0/hr
```

### Dependencies

#### [gspread](http://gspread.readthedocs.io/en/latest/)
```python
pip install gspread
```