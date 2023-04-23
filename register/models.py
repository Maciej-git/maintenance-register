from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class User(AbstractUser):
    MANAGER = 1
    TECHNICIAN = 2
    REQUESTER = 3

    ROLE_CHOISES = (
        (MANAGER, 'Manager'),
        (TECHNICIAN, 'Technician'),
        (REQUESTER, 'Requester')
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOISES, blank=True, null=True)

class Location(models.Model):
    name = models.CharField(max_length = 64, default = "Unknown")
    

    def __str__(self):
        return f"{self.name}"
    
class Area(models.Model):
    location = models.ForeignKey(Location, on_delete = models.CASCADE, related_name = "detailedLocation")
    name = models.CharField(max_length = 64, default = "Unknown")

    def __str__(self):
        return f"{self.name}" 
    
class Group(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Machine(models.Model):
    manufacturer = models.CharField(max_length = 64)
    type = models.CharField(max_length = 64)
    sn = models.CharField(max_length = 64)
    const_year = models.SmallIntegerField(default=2023, validators=[MaxValueValidator(9999), MinValueValidator(1900)])
    intern_symbol = models.CharField(max_length = 64)
    intern_no = models.SmallIntegerField(validators=[MaxValueValidator(9999), MinValueValidator(1)], null=True)

    EXCELLENT = 1
    GOOD = 2
    FAIR = 3
    POOR = 4

    CONDITION_CHOISES = [
        (EXCELLENT, 'Excellent'),
        (GOOD, 'Good'),
        (FAIR, 'Fair'),
        (POOR, 'Poor')
    ]

    condition = models.PositiveSmallIntegerField(choices = CONDITION_CHOISES, default = GOOD)
    location = models.ForeignKey(Location, on_delete = models.SET_DEFAULT, default = "Not defined", related_name = "area")
    group = models.ForeignKey(Group, on_delete = models.SET_DEFAULT, default = "Not specified", related_name = "category")

    def __str__(self):
        return f'{self.manufacturer} {self.type} {self.intern_symbol}{self.intern_no}'

class Request(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "userRequest", null=True)
    technician = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "technicianRequest", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    closeDate = models.DateTimeField(null=True, blank=True)
    machine = models.ForeignKey(Machine, on_delete = models.CASCADE, related_name = "machineRequest")
    issue = models.TextField()

    NEW = 1
    ONGOING = 2
    HOLD = 3
    CLOSED = 4

    STATUS_CHOICES = [
        (NEW, 'New request'),
        (ONGOING, 'Start work'),
        (HOLD, 'Hold'),
        (CLOSED, 'Done')
    ]

    status = models.PositiveSmallIntegerField(choices = STATUS_CHOICES, default = NEW) 

    def __str__(self):
        return f'{self.id} {self.machine.manufacturer} {self.machine.type}'
    
class Note(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=True)
    request = models.ForeignKey(Request, on_delete = models.CASCADE, related_name = "noteRequest")
    technician = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "noteTechnician", null=True)
    text = models.TextField()

    def __str__(self):
        return f'{self.request.id} {self.request.technician}'
