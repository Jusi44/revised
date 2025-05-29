# workouts/tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_scheduled_email(to_email):
    message = (
        "⏰ It's time to workout!\n\n"
        "Your body will thank you for it. Let's get moving! 💪\n\n"
        "Remember, consistency is key to achieving your fitness goals. "
        "Every workout counts, and you're one step closer to a healthier you!\n\n"
        "Stay motivated and keep pushing your limits!\n\n"
        "Best,\n"
        "Fitnotify Team"
    )

    send_mail(
        subject="⏰ Time to workout!",
        message=message,
        from_email='Fitnotify <no-reply@fitnotify.com>',
        recipient_list=[to_email],
        fail_silently=False,
    )
