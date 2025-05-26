# workouts/management/commands/send_notifications.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from workouts.models import Notification
from django.conf import settings

class Command(BaseCommand):
    help = "Send workout reminder emails to users when it’s time"

    def handle(self, *args, **options):
        now = timezone.localtime()
        current_hour   = now.hour
        current_minute = now.minute
        weekday_map = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        today_code  = weekday_map[now.weekday()]

        qs = Notification.objects.filter(
            time_hour=current_hour,
            time_minute=current_minute,
            days__contains=today_code  # MultiSelectField stores comma-sep
        )
        for notif in qs:
            profile = getattr(notif.user, 'profile', None)
            if profile and profile.notify_email:
                send_mail(
                    subject="⏰ Time to workout!",
                    message=(
                        f"Hey {notif.user.username}!\n\n"
                        "It's your scheduled workout time. Your body will thank you! 💪"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[profile.notify_email],
                    fail_silently=True,
                )
