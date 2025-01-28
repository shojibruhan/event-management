from django.db import models



class Category(models.Model):
    name= models.CharField(max_length=250)
    description= models.TextField()



class Participant(models.Model):
    name= models.CharField(max_length=100)
    email= models.EmailField(unique=True)
# Event:
#     name,
#     description,
#     date,
#     time,
#     location,
#     category(Foreign Key)


class Event(models.Model):
    category= models.ForeignKey(
        Category,
        on_delete=models.CASCADE, 
        default=2
    )
    participant= models.ManyToManyField(Participant, related_name='events')
    name= models.CharField(max_length=250)
    description= models.TextField(max_length=300)
    schedule= models.DateField()
    is_completed= models.BooleanField(default= False)
    created_at= models.DateTimeField(auto_now_add= True)
    updated_at= models.DateTimeField(auto_now= True)
    location= models.TextField()
    

class EventDetails(models.Model):
    CONCERT= 'C'
    HACKATHON= 'H'
    SEMINAR= 'S'
    FEST= 'F'
    OPTIONS= (
        (CONCERT, 'Concert'),
        (HACKATHON, 'Hackathon'),
        (SEMINAR, 'Seminar'),
        (FEST, 'Fest')
        
    )
    events= models.OneToOneField(
        Event, 
        on_delete=models.CASCADE,
        related_name='details')
    types= models.CharField(max_length=1, choices=OPTIONS)    
    participent= models.CharField(max_length=250)
# Participant:
#     name,
#     email,
#     Event(ManytoMany)


#     events= models.ManyToManyField(Event)

