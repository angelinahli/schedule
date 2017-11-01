## Scheduling app
Small program that pulls information for a to-do list I have on my spreadsheet, and then prints out a curated to do list for the amount of time I have to work today.

### Sample console output

```
user$ python run.py
How much time do you have today? (in hours) 9

DATE: 2017-11-01

TO DO:

1. Urgent important task 
    - est. time: 2.0 hours 
    - bang 4 buck: $125.0/hr
    - due: Thu Nov 02

2. Urgent, non important task 
    - est. time: 3.0 hours 
    - bang 4 buck: $16.67/hr
    - due: Wed Nov 01

3. Really important task 
    - est. time: 3.0 hours 
    - bang 4 buck: $166.67/hr
    - due: Sat Nov 04

4. Trivial task 
    - est. time: 4.0 hours 
    - bang 4 buck: $17.5/hr
    - due: Tue Nov 07
```

### Dependencies

#### [gspread](http://gspread.readthedocs.io/en/latest/)
```python
pip install gspread
```