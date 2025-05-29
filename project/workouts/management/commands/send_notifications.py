from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from workouts.models import Notification
from users.models import Profile  # adjust if needed
import pytz
from datetime import datetime

class Command(BaseCommand):
    help = 'Send workout reminder emails'

    def handle(self, *args, **kwargs):
        now = datetime.now(pytz.timezone('Asia/Manila'))
        current_hour = now.hour
        current_minute = now.minute
        current_day = now.strftime('%a')  # e.g. 'Mon', 'Tue'

        notifications = Notification.objects.filter(
            time_hour=current_hour % 12 if current_hour % 12 else 12,
            time_minute=current_minute,
        )

        for notif in notifications:
            if current_day in notif.days:
                profile = getattr(notif.user, 'profile', None)
                if profile and profile.notify_email:
                    send_mail(
                        subject="⏰ Time to workout!",
                        message=(
                            f"Hi {notif.user.username},\n\n"
                            "⏰ It's time to workout!\n\n"
                            "Your body will thank you for it. Let's get moving! 💪\n\n"
                            "Stay consistent!\n\n— FitNotify"
                        ),
                        from_email='Fitnotify <no-reply@fitnotify.com>',
                        recipient_list=[profile.notify_email],
                        fail_silently=False,
                    )
