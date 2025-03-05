from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from tasks.models import RSVP
from users.models import UserProfile


@receiver(post_save,  sender= User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        token= default_token_generator.make_token(instance)
        activation_url= f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"

        subject= "Activation E-mail"
        message= f"Hello {instance.username},\n\nPlease activate your email through this link:\n\n{activation_url}\n\nThank You\nTeam Event Management"
        recipient_list= [instance.email]

        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        except Exception as e:
            print(f"Faild to send mail to  {instance.email}: {str(e)}")

@receiver(post_save, sender= User)
def assign_role(sender, instance, created, **kwargs):
    if created:
        user_groups, created= Group.objects.get_or_create(name= "Participant")
        instance.groups.add(user_groups)
        instance.save()

@receiver(post_save,  sender= RSVP)
def send_invitation_mail(sender, instance, created, **kwargs):
    if created:
        subject= "Invitation E-mail"
        message= f"Hello {instance.user.first_name},\n\nYou are invited to the upcoming {instance.event.name}.\n\nThanks."
        recipient_list= [instance.user.email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

@receiver(post_save, sender= User)
def create_or_update_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user= instance)