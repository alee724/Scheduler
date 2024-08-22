# Scheduler
Scheduler backend development using python. Finished the backend work for the scheduler sheet. Will have to work on implementing a server for multiple connections and the issue of multiple commands coming in at once. I also want to develop a connection to google drive to maintain a longer term data base for accessing perhaps years worth of data. 

# TODO:
- make a server 
    - perhaps instead do ssh by making the ip static and making it such that you can connect to a certain computer from home 
- connect to google drive 
- need to retest the service, customer, and employee modules as I needed to changed the __eq__ definition
- change the entries in the customer pop up to comboboxes so that we can search for a customer with an input and automatically input data
- need to test saving and loading a day 

# ISSUES:
- need to fix up a lot of the comments 
- need for optimizing code in a lot of places, mostly backend 
- issue of layering frames causing customer frames to appear above employee frames

# NOTES: 
- maybe change column.py such that the place holders are not all 0s but scale with "distance" from the item index 
- may use the toast module in the ttkbootstrap for notifications from outside sources, i.e. a phone call, payments from card reader, etc.

# IMPORTANT:
- need to add scroll region LAST no matter what. Else it starts messing with the scroll region leading it to go kinda everywhere but where you want it to be 
- ...upgrading python seems to have solved the button issues... sigh
- one my biggest mistakes yet may be not using the #TODO tag where I made comments about further working on things...


# Virtual Events:       
- This is here to keep track of all the virtual events I am making and to make sure there is no overlap of events or such 
- <<VerifyAddColumn>>, when sending data from the popup to the sheet frame 
- <<AddColumn>>, can be seen as a duplicate of the "<<AddEmployeeColumn>>" event, will see if it can be replaced 
- <<AddEmployee>>, resizes the employee label canves and sets the scroll region, again, may be a duplicate 

- <<VerifyAddCustomer>>, when adding a customer from the popup, not a duplicate 
- <<VerifyMoveCustomer>>, when moving a customer, not a duplicate  
- <<VerifyDestroyCustomer>>, when getting rid of a customer, there is an issue of raising an error for some reason I don't know
- <<VerifyServed>>, need to add the checking process with the json sheet and changing the data but otherwise works as intended
- <<UpdateService>>, locally updates the list of services in the json file 
- <<UpdateSchedule>>, locally updates the schedule dictionary of employees throughout the week 
- <<UpdateCustomers>>, locally updates the list of customers 
