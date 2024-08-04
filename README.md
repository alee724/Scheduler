# Scheduler
Scheduler backend development using python. Finished the backend work for the scheduler sheet. Will have to work on implementing a server for multiple connections and the issue of multiple commands coming in at once. I also want to develop a connection to google drive to maintain a longer term data base for accessing perhaps years worth of data. 

# TODO:
- make the front end, the gui 
    - maybe into a website later on 
- make a server 
    - perhaps instead do ssh by making the ip static and making it such that you can connect to a certain computer from home 
- connect to google drive 

# ISSUES:
- have not tried synching the backend and front end as of yet
    - need a better way to get boolean responses from the backend

# NOTES: 
- maybe change column.py such that the place holders are not all 0s but scale with "distance" from the item index 

# IMPORTANT:
- need to add scroll region LAST no matter what. Else it starts messing with the scroll region leading it to go kinda everywhere but where you want it to be 
