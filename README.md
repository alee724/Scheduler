# Scheduler
Scheduler backend development using python. Finished the backend work for the scheduler sheet. Will have to work on implementing a server for multiple connections and the issue of multiple commands coming in at once. I also want to develop a connection to google drive to maintain a longer term data base for accessing perhaps years worth of data. 

TODO:
- make a server 
- connect to google drive 
- create a gui for the scheduler 
- modify the customer class such that you can split it into multiple customers with the same attributes except for the fact that the list of services have been split, should be done from the sheet module 
- DBMS for the schedule sheet, more specifically for the customers and services, employees perhaps as well tho all they need is a string for their name  


ISSUES:

NOTES: 
- maybe change the columns such that the place holders are not all 0s but scale with "distance" from the item index 
