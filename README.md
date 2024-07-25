# Scheduler
Scheduler backend development using python. Finished the backend work for the scheduler sheet. Will have to work on implementing a server for multiple connections and the issue of multiple commands coming in at once. I also want to develop a connection to google drive to maintain a longer term data base for accessing perhaps years worth of data. 

# TODO:
- need to make an intermediary module for taking string inputs and modifying the sheet 
    - for example a string input of values for a customer with some string input of services 
- make a json file for containing all customers and all services 
- need to be able to take these from a dbms with MySQL probably 
- make a server 
    - perhaps instead do ssh by making the ip static and making it such that you can connect to a certain computer from home 
- connect to google drive 
- create a gui for the scheduler 
- DBMS for the schedule sheet, more specifically for the customers and services, employees perhaps as well tho all they need is a string for their name  


# ISSUES:

# NOTES: 
- maybe change the columns such that the place holders are not all 0s but scale with "distance" from the item index 
