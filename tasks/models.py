from django.db import models


class Category(models.Model):
    name= models.CharField(max_length=250)
    description= models.TextField()

    def __str__(self):
        return self.name

class Participant(models.Model):
    name= models.CharField(max_length=100)
    email= models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    UPCOMING_EVENTS= 'U'
    PAST_EVENTS= 'P'
    STATUS_CHOICES = [
        (UPCOMING_EVENTS, 'Upcoming Events'),
        (PAST_EVENTS, 'Past Events')
    ]


    category= models.ForeignKey(
        Category,
        on_delete=models.CASCADE, 
        default=1
    )
    participant= models.ManyToManyField(Participant, related_name='events')
    name= models.CharField(max_length=250)
    description= models.TextField()
    schedule= models.DateField()
    status= models.CharField(max_length=20, choices=STATUS_CHOICES, default= UPCOMING_EVENTS)
    is_completed= models.BooleanField(default= False)
    created_at= models.DateTimeField(auto_now_add= True)
    updated_at= models.DateTimeField(auto_now= True)
    location= models.CharField()

    def __str__(self):
        return self.name



    

    

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
    asset= models.ImageField(upload_to='tasks_asset', blank=True, null= True, default='tasks_asset/default.jpg')
    types= models.CharField(max_length=1, choices=OPTIONS)    
    participent= models.CharField(max_length=250)

    def __str__(self):
        return f"Details for the Events {self.events.name}"
    