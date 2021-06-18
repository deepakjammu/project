from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Report(models.Model):
    loc = (
        ('CH','Corporate Headoffice'),
        ('OD','Operations Department'),
        ('WS','Work Station'),
        ('MD','Marking Division')
        )

    sv = (
        ('M','Mild'),
        ('MD','Moderate'),
        ('S','Severe'),
        ('F','Fetal')
    )
   

    incident_department = models.CharField( max_length=2,choices=loc)
    description = models.CharField(max_length=250)
    date  = models.DateField( auto_now=False, auto_now_add=False)
    time = models.TimeField( auto_now=False, auto_now_add=False)
    incident_location = models.TextField()
    severity = models.CharField(max_length=10, choices=sv)
    
    cause = models.TextField()
    actions=models.TextField()
    type_env = models.CharField( max_length=10)
    type_inju = models.CharField( max_length=10)
    type_property = models.CharField( max_length=10,default="f")
    type_vehicle = models.CharField( max_length=10,default="f")
    reportedby_id = models.CharField(max_length=10)


