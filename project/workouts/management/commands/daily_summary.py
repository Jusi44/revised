# workouts/management/commands/daily_summary.py

from django.core.management.base import BaseCommand
from django.core.mail          import send_mail
from django.conf               import settings
from django.contrib.auth.models import User
from workouts.models           import WorkoutSession
from datetime                  import date, timedelta

class Command(BaseCommand):
    help = "Email each user their yesterday's workout summary"

    def handle(self, *args, **opts):
        yesterday = date.today() - timedelta(days=1)

        for user in User.objects.all():
            # grab all sessions completed yesterday
            sessions = WorkoutSession.objects.filter(
                user=user,
                completed_at__date=yesterday
            )
            if not sessions.exists():
                continue  # nothing to report

            total_minutes = sum(s.duration_minutes for s in sessions)
            exercise_lines = "\n".join(
                f"- {s.exercise_name}: {s.duration_minutes} min"
                for s in sessions
            )

            subject = f"Your FitNotifiy summary for {yesterday:%b %d, %Y}"
            message = (
                f"Hi {user.get_full_name() or user.username},\n\n"
                f"Yesterday you did {len(sessions)} workouts totalling {total_minutes} minutes:\n\n"
                f"{exercise_lines}\n\n"
                "Keep it up!\n\n"
                "— The FitNotifiy Team"
            )

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False
            )

            self.stdout.write(f"Sent summary to {user.email}")
