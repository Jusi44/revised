from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.utils import timezone

DAYS_OF_WEEK = (
    ('Mon', 'Monday'),
    ('Tue', 'Tuesday'),
    ('Wed', 'Wednesday'),
    ('Thu', 'Thursday'),
    ('Fri', 'Friday'),
    ('Sat', 'Saturday'),
    ('Sun', 'Sunday'),
)

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20)
    steps = models.TextField()
    image = models.ImageField(upload_to='exercise_images/')

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class WorkoutSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=100, default='Rest Day')
    duration_seconds = models.PositiveIntegerField()
    completed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} – {self.exercise_name} ({self.duration_seconds} sec)"

    @property
    def duration_str(self):
        secs = self.duration_seconds
        if secs < 60:
            return f"{secs} sec"
        mins, rem = divmod(secs, 60)
        if rem:
            return f"{mins} min {rem} sec"
        return f"{mins} min"



    @property
    def duration_minutes(self):
        # integer minutes
        return self.duration_seconds // 60

    @property
    def duration_remainder_seconds(self):
        # leftover seconds
        return self.duration_seconds % 60

    def __str__(self):
        return f"{self.user.username} - {self.exercise_name} ({self.duration_seconds}s)"



class UserStreak(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_streak = models.PositiveIntegerField(default=0)
    last_workout_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.current_streak} days"
    
    @property
    def duration_minutes(self):
        return self.duration_seconds // 60

class Notification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    days = MultiSelectField(choices=DAYS_OF_WEEK)
    time_hour = models.IntegerField(default=8)
    time_minute = models.IntegerField(default=0)  # ✅ FIXED


