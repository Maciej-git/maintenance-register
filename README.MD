# **Capstone: Maintenance register - Web based CMMS application to manage repair requests**
### **Video Demo:**  https://youtu.be/caVBp8DDhqk
### **Description:**

The application is web based, implemented with Python (Django framework) and JavaScript, dedicated to help teams plan, manage and execute work orders efficiently. The core idea is CMMS (Computerised Maintenance Management Systems) and the main functionality is to track requests, assignments, and completed tasks all in one place.

### **Distinctiveness and Complexity:**

Application functionality is based on my work experience as a maintenance engineer in an industrial automation environment. Maintenance management requires efficient information exchange within team-members and company departments to save time, reduce costs and increase equipment availability. To make it possible, every user of the application, has assigned 1 of the 3 roles:

* Requestor - default user role, which allow raising a new repair request and check the status
* Technician - user role, which allows accepting, proceed and close the repair request and have access to machine database
* Manager - user role, which allows monitoring, manage, assign and reassign repair requests and manage machine database

### **How to run the application:**

1. In terminal navigate to maintenance project directory.
2. Run 'python3 manage.py makemigrations' to make migrations for the register app.
3. Run 'python3 manage.py migrate' to apply migrations to database.
4. Optionally: run 'python3 manage.py create superuser' to create superuser account, which will allow to change the user role in User Model.
5. Run 'python3 manage.py runserver' to run the application locally.


### **Specification of views in main application file - views.py**

#### **register_view**

Allows a user to register for an account via a form, with default role "Requestor".

#### **login_view**

Allows a registered user to log and redirects to index if succeeded.

#### **logout_view**

Allows a registered user to logout.

#### **index**

Default route from register/urls.py loads an index function, which renders the register/index.html template, as long as user is signed in or if not, redirects to login_view. The template stored at register/templates/register/index.html extends the layout.html, which is based on Bootswatch Lux Theme (https://bootswatch.com/), as all the other HTML documents in this project. This helps to simplify the design, styling and responsive functionality and allows concentrating on core functionality. 
Django template instructions determines which parts of HTML document needs to be rendered accord to user role and provide required functionality. JavaScript is used to make the website more interactive and user-friendly. 
The functionality vary of role assigned to user:  

* "Requestor" can monitor status of her/his requests and have access to already completed tasks from the past.
* "Technician" can accept and handle and monitor the repair requests, hold the task if any problem occurs (e.g. repair needs the spare part, which is not available). This step requires writing a note, containing the reason of holding the task, to keep the team-members informed. 
Finally, "Technician" can change task status to "complete" after work is done. User with this role can also access to all archived requests and notes.
* "Manager" can assign or reassign tasks to "Technician" and monitor all the requests.

A repair request can have one of 4 status state:
* "New"
* "Ongoing"
* "Hold"
* "Completed"

index.html uses JavaScript stored at register/static/register:

### requests.js

This script allows switching between the views of task categories, which improves the readability of the presented data.

### update.js

This script updates the "New" status tasks list with the interval of 1 minute. This prevents of need to manually refresh of whole webpage to check for any new tasks. JavaScript updates the new task counter, which is presented to the user and if there are no new tasks then shows the date and time of last check.
The second function of this script is to fetch the notes related to the repair request selected by the user. This prevents from need to load all notes. Displayed notes can be hidden after checking, which improves readability.

#### **request**

This function renders request.html from the templates and gives the ability to raise a new repair request with a Django ModelForm 'newRequest' stored at register/forms.py, which takes data fields from 'Request' model stored at register/models.py.

#### **machine**

This function has an 'activity' parameter from a route stored at register/urls.py, and is available only for users with "Technician" and "Manager". This 'activity' parameter can have 3 values, which determines functionality: 

* 'add' : renders addMachine.html from templates and gives the ability to add a new machine to database with a Django ModelForm 'machineForm' stored at register/forms.py, which takes data fields from 'Machine' model stored at register/models.py

* 'locations' : renders locations.html from templates and gives the ability to add a new location to the database with a 'Location' model stored at register/models.py. It also includes 'Area' and 'Group' models, which allows describing the machines locations more precise.

locations.html uses JavaScript stored at register/static/register:

### groups.js

This script allows switching between the views of location categories, which improves the readability of the presented data. It also updates the list of groups related to currently chosen location, without page reloading.
Finally, sends data via 'POST' request with 'csrf token' in header to fulfil Django Cross Site Request Forgery protection, also without the need of page reloading.

* 'select' : if approached via GET request, renders select.html from templates and gives the ability to search for machines in database.

select.html uses JavaScript stored at register/static/register:

### types.js

This script limits the machine type select list accordingly to the chosen manufacturer and improves user experience.

If approached via POST request, renders results.html from templates and shows the search results.

results.html uses JavaScript stored at register/static/register:

### check.js

This script updates the count of requests assigned to a selected machine without the need of page reloading.

#### **dataAPI**

Application API route:

* Sending GET request to /data?q=<location_name> where <location_name> is a name from 'Location' model, stored at register/models.py, will return a list (in JSON form) of all areas assigned to that location

* Sending GET request to /data?mfr=<manufacturer_name> where <manufacturer_name> is a name from 'Machine' model, stored at register/models.py will return a list (in JSON form) of all machine types related to manufacturer's name

* Sending GET request to /data?id=<machine_id> where <machine_id> is id from 'Machine' model, stored at register/models.py will return a list (in JSON form) of requests counts divided by status and related to queried machine_id

#### **updateAPI**

Application API route:

* Sending GET request to /update?q=<update_item> where <update_item> is either 'newtasks' or 'notes&id=<request_id>' (<request_id> is id from 'Request' model stored at register/models.py) will return HTML response, which is used by JavaScript (update.js stored at register/static/register) to update website content without the need of manual refreshing.