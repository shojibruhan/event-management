import os
import django
from faker import Faker
import random
from tasks.models import Category, Participant, Event, EventDetails

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

# Function to populate the database
def populate_db():
    # Initialize Faker
    fake = Faker()

    # Create Categories
    categories = [Category.objects.create(
        name=fake.bs().capitalize(),
        description=fake.paragraph(),
    ) for _ in range(5)]
    print(f"Created {len(categories)} categories.")

    # Create Participants
    participants = [Participant.objects.create(
        name=fake.name(),
        email=fake.email()
    ) for _ in range(10)]
    print(f"Created {len(participants)} participants.")

    # Create Events
    events = []
    for _ in range(20):
        event = Event.objects.create(
            category=random.choice(categories),
            name=fake.sentence(),
            description=fake.paragraph(),
            schedule=fake.date_this_year(),
            status=random.choice(['U', 'P']),  # Use actual model choices
            is_completed=random.choice([True, False]),
            location=fake.city()
        )
        event.participant.set(random.sample(participants, random.randint(1, 3)))  # Fix field name
        events.append(event)
    print(f"Created {len(events)} events.")

    # Create EventDetails
    for event in events:
        EventDetails.objects.create(
            events=event,  # Fix field name
            types=random.choice(['C', 'H', 'S', 'F']),  # Use actual model choices
            participent=", ".join([person.name for person in event.participant.all()]),  # Fix participant names
        )
    print("Populated EventDetails for all events.")
    print("Database populated successfully!")

