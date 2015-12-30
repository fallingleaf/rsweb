from django.core.mail import send_mail, BadHeaderError
from celery.task import task

@task
def send_message(from_email, to_emails, message, subject='New Message'):
    try:
        send_mail(subject, message, from_email, to_emails, fail_silently=False)
    except Exception as e:
        print e
        return False
        
    return True