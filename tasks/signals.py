from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.core.mail import send_mail
from tasks.models import Event


@receiver(m2m_changed, sender= Event.participant.through)
def notify_perticipents_on_event_creation(sender, instance, action, **kwargs):
    if action == "post_add":
        assigned_emails= [person.email for person in instance.participant.all()]
        send_mail(
            "New Event Launched",
            f"Yor are invited to attend to {instance.name}",
            'si.ruhan09@gmail.com',
            assigned_emails
        )
