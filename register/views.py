from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import User, Location, Group, Machine, Area, Request, Note
from register.forms import MachineForm, selectMachine, newRequest, newNote
from django.db import IntegrityError
from datetime import datetime

import json


# Render main view if user is authenticated, otherwise render login view.
def index(request):
    
    if request.method == "POST":
        if request.POST["statusTask"] == 'hold':
            taskForm = request.POST["request"]
            technicianForm = request.POST["technician"]
            text = request.POST["text"]
            task = Request.objects.get(pk=taskForm)

            # Change task status to Hold
            task.status = 3
            technician = User.objects.get(pk=technicianForm)

            # Create new note
            note = Note(request=task, technician=technician, text=text)

            # Save changes 
            note.save()
            task.save()
            
        elif request.POST["statusTask"] == 'resume':
            taskID = request.POST["resumeTask"]
            task = Request.objects.get(pk=taskID)

            # Change back task status to "Ongoing"
            task.status = 2
            task.save()

        elif request.POST["statusTask"] == 'accept':
            taskID = request.POST["taskID"]
            task = Request.objects.get(pk=taskID)

            if request.user.role == 1:
                technicianID = request.POST["assignTechnician"]
                technician = User.objects.get(pk=technicianID)
                

            # Assign technician to task and Change status to "Ongoing"
            if request.user.role == 2:
                task.technician = request.user
            elif request.user.role == 1:
                task.technician = technician

            task.status = 2
            task.save()

        elif request.POST["statusTask"] == 'complete':
            taskID = request.POST["taskID"]
            task = Request.objects.get(pk=taskID)
            task.technician = request.user
            task.status = 4
            task.closeDate = datetime.now()
            task.save()

        return HttpResponseRedirect(reverse("index"))

    if request.user.is_authenticated:
        if request.user.role == 2 or request.user.role == 1:
            requests = Request.objects.all()
            technicians = User.objects.filter(role = 2)
            
        else:
            requests = Request.objects.filter(user = request.user)
            technicians = None
        
        # Count requests with status = "New"
        newTasks = 0
        for task in requests:
            if task.status == 1:
                newTasks += 1
                print(f"Selected task id= {task.id} counter= {newTasks}")
                
        print(f"{len(requests)} tasks, {newTasks} are new")
        form = newNote()
         
        return render(request,"register/index.html", {'requests': requests, 'newTasks': newTasks, 'form': form, 'technicians': technicians})
    else:
        return login_view(request)

# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # If user authenticate sucecessfuly redirect to index, otherwise render login view with error message 
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "register/login.html", {"message": "Invalid username and/or password."})
    else:
        return render(request, "register/login.html")

# Logout view
def logout_view(request):
    logout(request)
    return render(request, "register/logout.html")
    
# User register view
def register(request):
    if request.method == "POST":
        name = request.POST["name"]
        lastname = request.POST["lastname"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Check if password and confirmation matches
        if password != confirmation:
            return render(request, "register/register.html", {'message': "Passwords must match."})

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = name
            user.last_name = lastname
            user.save()
        except IntegrityError:
            return render(request, "register/register.html", {'message': "Username already taken."})
        
       
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register/register.html")

# Machine view
def machines(request, activity):
    # Add new machine to database
    if activity == 'add':
        if request.method == 'POST':
            form = MachineForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponse('Sorry, error...')
        else:
            form = MachineForm()
            return render(request, "register/addMachine.html", {'form': form})
        
    # Add new location to database    
    elif activity == 'locations':
        
        if request.method == 'POST':
            data = json.loads(request.body)
            subject = data["subject"]
            item = data["item"]
            if subject == "main":
                location = Location(name = item)
                location.save()
                return JsonResponse({"message": "OK"}, status=200)
            elif subject == "areas":
                mainLocation = Location.objects.filter(name = data["location"])
                area = Area(location = mainLocation[0], name = item)
                area.save()
                return JsonResponse({"message": "OK"}, status=200)
            elif subject == "groups":
                group = Group(name = item)
                group.save()
                return JsonResponse({"message": "OK"}, status=200)
            
        locations = Location.objects.all()
        groups = Group.objects.all()
        areas = Area.objects.all()
        return render(request, "register/locations.html", {'locations': locations, 'areas': areas,'groups': groups})
    
    # Select machine
    elif activity == 'select':
        if request.method == 'POST':

            # Create dictionary of all items from POST
            items = (dict(request.POST.items()))
           
            # Delete csrf token from items
            del items['csrfmiddlewaretoken']
           
            # Create filters dictionary: select keys with non blank values
            filters = {}
            for key, value in items.items():
                if value != '':
                    filters.update({key : value})
            print(f"Active filters are: {filters}")
            
            # Check if location is in active filters, then replace location name with id from Location model instance
            if 'location' in filters.keys():
                locationID = Location.objects.get(name=filters['location'])
                filters['location'] = locationID.id
                
             
            # Use filters on machine model
            machines = Machine.objects.filter(**filters)
          
            return render(request, "register/results.html", {'machines': machines})
        
        # Create machine manufacturers list
        machines = Machine.objects.all()
        mfrList = []
        for machine in machines:
            mfrList.append(machine.manufacturer)

        # Use set to eliminate dupicated manufacturer names
        mfr_set = set(mfrList)

        # Create location list
        locations = Location.objects.all()
       
        return render(request, "register/select.html", {'manufacturers': mfr_set, 'locations': locations})

    else:
       return HttpResponse('Sorry, error...')

# Data API 
def dataAPI(request):
    q = request.GET.get('q')
    mfr = request.GET.get('mfr')
    id = request.GET.get('id')
    if q != None:
        location = Location.objects.filter(name = q)
        areas = Area.objects.filter(location = location[0])
        names = []
        for area in areas:
            names.append(area.name)
        return JsonResponse({"areas": names}, status = 200)
    elif mfr != None:
        machines = Machine.objects.filter(manufacturer = mfr)
        types = []
        for machine in machines:
            types.append(machine.type)

        return JsonResponse({"types": types}, status = 200)
    elif id != None:
        machine = Machine.objects.get(pk=id)
        tasks = Request.objects.filter(machine=machine)

        newTasks = 0
        ongoingTasks = 0
        completedTasks = 0

        for task in tasks:
            if task.status == 1:
                newTasks += 1
            elif task.status == 2 or task.status == 3:
                ongoingTasks += 1
            elif task.status == 4:
                completedTasks += 1

        return JsonResponse({'new': newTasks, 'ongoing': ongoingTasks, 'completed': completedTasks}, status=200)

    else:
        return HttpResponse("Sorry, error...")
    
# Request view
def request(request):
    if request.method == "POST":
       machineForm = request.POST["machine"]
       issueForm = request.POST["issue"]
       print(machineForm + ' ' + issueForm)
       machine = Machine.objects.get(pk=machineForm)
       user = User.objects.get(pk=request.user.id)
       task = Request(user=user, machine=machine, issue=issueForm)
       task.save()
       return HttpResponseRedirect(reverse("index"))
    else:
        form = newRequest()
        return render(request, "register/request.html", {'form': form})

def updateAPI(request):
    q = request.GET.get('q')
   
    if q == 'newtasks':
        tasks = Request.objects.filter(status=1)
        technicians = User.objects.filter(role=2)
        newTasks = len(tasks)
        return render(request, "register/update.html", {'tasks': tasks, 'newTasks': newTasks, 'technicians': technicians})
    elif q == 'notes':
         id = request.GET.get('id')
         task = Request.objects.get(pk=id)
         notes = Note.objects.filter(request=task).order_by("-date")
         return render(request, "register/notes.html", {'notes': notes, 'id': id})



