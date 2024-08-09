# Scheduler
Scheduler backend development using python. Finished the backend work for the scheduler sheet. Will have to work on implementing a server for multiple connections and the issue of multiple commands coming in at once. I also want to develop a connection to google drive to maintain a longer term data base for accessing perhaps years worth of data. 

# TODO:
- make the front end, the gui 
    - maybe into a website later on 
- make a server 
    - perhaps instead do ssh by making the ip static and making it such that you can connect to a certain computer from home 
- connect to google drive 
- need to retest the service, customer, and employee modules as I needed to changed the __eq__ definition
- Need to try to send data via an event generated, for customers, hopefully that is possible, if not via an intermediary somehow

# ISSUES:
- have not tried synching the backend and front end as of yet
    - need a better way to get boolean responses from the backend

# NOTES: 
- maybe change column.py such that the place holders are not all 0s but scale with "distance" from the item index 
- may use the toast module in the ttkbootstrap for notifications from outside sources, i.e. a phone call, payments from card reader, etc.

# IMPORTANT:
- need to add scroll region LAST no matter what. Else it starts messing with the scroll region leading it to go kinda everywhere but where you want it to be 
- ...upgrading python seems to have solved the button issues... sigh
