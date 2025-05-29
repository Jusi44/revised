import time
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.core.mail import send_mail


EXERCISES = {
    "Push-Up": {
        "difficulty": "Medium",
        "steps": [
            "Start in a plank position with your arms straight.",
            "Lower your body until your chest nearly touches the floor.",
            "Push yourself back up to the starting position.",
            "Repeat for desired reps."
        ],
        "image": "pushup.jpg"
    },
    "Squat": {
        "difficulty": "Easy",
        "steps": [
            "Stand with feet shoulder-width apart.",
            "Lower your body by bending your knees and pushing hips back.",
            "Keep your chest up and knees behind toes.",
            "Rise back to standing position.",
            "Repeat for desired reps."
        ],
        "image": "squat.jpg"
    },
    "Plank": {
        "difficulty": "Medium",
        "steps": [
            "Start on your forearms and toes, keeping your body straight.",
            "Engage your core and hold the position.",
            "Keep your hips from sagging or rising.",
            "Hold for the desired duration."
        ],
        "image": "plank.jpg"
    },
    "Lunges": {
        "difficulty": "Medium",
        "steps": [
            "Stand upright with feet hip-width apart.",
            "Step forward with one leg and lower your hips until both knees are bent at 90 degrees.",
            "Return to starting position.",
            "Switch legs and repeat."
        ],
        "image": "lunges.jpg"
    },
    "Burpees": {
        "difficulty": "Hard",
        "steps": [
            "Begin in a standing position.",
            "Drop into a squat with your hands on the ground.",
            "Kick your feet back into a plank position.",
            "Perform a push-up.",
            "Jump your feet back to squat position.",
            "Jump up with arms extended overhead."
        ],
        "image": "burpees.jpg"
    },
    "Mountain Climbers": {
        "difficulty": "Medium",
        "steps": [
            "Start in a plank position.",
            "Drive one knee toward your chest.",
            "Quickly switch legs, like running horizontally.",
            "Maintain a steady pace."
        ],
        "image": "mountain_climbers.jpg"
    },
    "Handstand Hold": {
        "difficulty": "Hard",
        "steps": [
            "Kick up into a handstand against a wall.",
            "Engage your core and keep your body straight.",
            "Hold the position as long as possible.",
            "Carefully come down."
        ],
        "image": "handstand_hold.jpg"
    },
    "Dips": {
        "difficulty": "Medium",
        "steps": [
            "Use parallel bars or a bench.",
            "Lower your body by bending your elbows until your shoulders are below your elbows.",
            "Push back up to the starting position.",
            "Repeat for desired reps."
        ],
        "image": "dips.jpg"
    },
    "Jumping Jacks": {
        "difficulty": "Easy",
        "steps": [
            "Stand upright with feet together and hands at your sides.",
            "Jump your feet out and raise your arms overhead.",
            "Jump feet back together and lower arms.",
            "Repeat rapidly."
        ],
        "image": "jumping_jacks.jpg"
    },
    "Bicycle Crunches": {
        "difficulty": "Medium",
        "steps": [
            "Lie on your back with hands behind your head.",
            "Bring opposite elbow to knee while extending the other leg.",
            "Alternate sides in a pedaling motion.",
            "Repeat for desired reps."
        ],
        "image": "bicycle_crunches.jpg"
    }
}



from .models import WorkoutSession

from datetime import date, timedelta
from .models import WorkoutSession, UserStreak
from users.models import Profile 


from django.shortcuts import redirect

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import WorkoutSession, UserStreak
from users.models import Profile
from datetime import date, timedelta

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import WorkoutSession, UserStreak
from users.models import Profile
from datetime import date, timedelta

@login_required
def dashboard(request):
    profile = request.user.profile

    # If the profile is complete, proceed with the dashboard logic
    user = request.user
    history = WorkoutSession.objects.filter(user=user).order_by('-completed_at')

    # Calculate streak
    try:
        streak_obj = UserStreak.objects.get(user=user)
        today = date.today()
        if streak_obj.last_workout_date == today or streak_obj.last_workout_date == today - timedelta(days=1):
            streak = streak_obj.current_streak
        else:
            streak = 0
    except UserStreak.DoesNotExist:
        streak = 0

    # Current exercise handling
    selected = request.session.get('selected_exercises', [])
    current_exercise = selected[0] if selected else None
    request.session['selected_exercises'] = []

    # Workout summary stats
    total_workouts = history.count()
    total_seconds = sum([session.duration_seconds for session in history])
    total_minutes = total_seconds // 60
    total_remainder_seconds = total_seconds % 60

    def estimate_calories(duration_seconds):
        MET = 3.0  # moderate intensity
        weight_kg = profile.weight or 20  # fallback weight if missing
        return int(MET * 3.5 * weight_kg / 200 * duration_seconds)

    total_calories = estimate_calories(total_seconds)

    # Recommended exercises logic based on profile data
    recommended_exercises = []
    if profile.sex == 'M':
        recommended_exercises = [
        'Push-ups (Beginner)',
        'Pull-ups (Intermediate)',
        'Burpees (Intermediate)',
        'Dips (Intermediate)',
        'Handstand Hold (Advanced)',
        'Mountain Climbers (Beginner)',
        'Plank to Push-up (Intermediate)',
        'Pike Push-ups (Advanced)',
        'Jump Squats (Intermediate)',
        'Chin-ups (Intermediate)'
    ]
    elif profile.sex == 'F':
        recommended_exercises = [
        'Squats (Beginner)',
        'Lunges (Beginner)',
        'Plank (Beginner)',
        'Glute Bridges (Beginner)',
        'Wall Sits (Intermediate)',
        'Step-ups (Beginner)',
        'Side Plank (Intermediate)',
        'Donkey Kicks (Beginner)',
        'Superman Hold (Intermediate)',
        'High Knees (Beginner)'
    ]

    else:
        recommended_exercises = []

    context = {
        'user': user,
        'history': history,
        'streak': streak,
        'selected_exercises': selected,
        'current_exercise': current_exercise,
        'total_workouts': total_workouts,
        'total_minutes': total_minutes,
        'total_remainder_seconds': total_remainder_seconds,
        'total_calories': total_calories,
        'recommended_exercises': recommended_exercises,  # Added here
    }
    return render(request, 'workouts/dashboard.html', context)








from .models import WorkoutSession, UserStreak
from datetime import date, timedelta

from .models import WorkoutSession

from datetime import date, timedelta
from .models import UserStreak
from django.views.decorators.csrf import csrf_exempt

@login_required
@csrf_exempt
def complete_workout(request):
    if request.method == 'POST':
        exercise_name = request.POST.get('exercise_name')
        duration = request.POST.get('duration')

        selected = request.session.get('selected_exercises', [])
        current_index = request.session.get('current_exercise_index', 0)

        # Prevent double submission
        last_logged = request.session.get('last_logged_index')
        if last_logged == current_index:
            return JsonResponse({'status': 'duplicate'})

        if exercise_name and duration:
            duration_seconds = int(duration)
            WorkoutSession.objects.create(
                user=request.user,
                exercise_name=exercise_name,
                duration_seconds=duration_seconds,
            )

            request.session['last_logged_index'] = current_index  # mark this as logged

            # Email logic
            profile = getattr(request.user, 'profile', None)
            recipient_email = profile.notify_email if profile else request.user.email
            if recipient_email:
                # Format the duration for the email
                if duration_seconds < 60:
                    duration_str = f"{duration_seconds} sec"
                else:
                    duration_minutes = duration_seconds // 60
                    duration_remainder_seconds = duration_seconds % 60
                    duration_str = f"{duration_minutes} minute" + ("s" if duration_minutes > 1 else "")
                    if duration_remainder_seconds > 0:
                        duration_str += f" and {duration_remainder_seconds} sec"

                # Create a more detailed message
                message = (
                    f"Hi {request.user.username},\n\n"
                    f"Congratulations on completing your workout! 🎉\n\n"
                    f"You just finished {exercise_name} for {duration_str}. "
                    f"Keep up the great work and stay consistent with your fitness journey!\n\n"
                    f"Remember, every workout counts towards your goals. "
                    f"Stay motivated and challenge yourself with each session!\n\n"
                    f"Best,\n"
                    f"Fitnotify Team"
                )

                send_mail(
                    subject='Workout Completed!',
                    message=message,
                    from_email='Fitnotify <no-reply@fitnotify.com>',  # Set the sender's name and email
                    recipient_list=[recipient_email],
                    fail_silently=False,
                )

            # Advance to next exercise
            if selected:
                selected.pop(0)  # Remove the completed exercise
                request.session['selected_exercises'] = selected

            request.session['current_exercise_index'] = 0
            request.session.pop('last_logged_index', None)

            return JsonResponse({'status': 'success'})

        return JsonResponse({'status': 'error', 'message': 'Missing data'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)











from django.shortcuts import render, redirect

def exercise(request):
    if request.method == 'POST':
        selected = request.POST.getlist('selected_exercises')
        request.session['selected_exercises'] = selected
        return redirect('dashboard')

    exercises = ["Push Up", "Plank", "Burpees", "Handstand"]  # Add more as needed
    selected_exercises = request.session.get('selected_exercises', [])
    return render(request, 'workouts/exercise.html', {
        'exercises': exercises,
        'selected_exercises': selected_exercises
    })





from django.shortcuts import render, redirect
from .models import Exercise

from django.shortcuts import redirect
from workouts.models import Exercise
from .models import WorkoutSession

def start_workout(request):
    selected_ids = request.session.get('selected_exercises', [])
    selected_exercises = Exercise.objects.filter(id__in=selected_ids)

    # Create a WorkoutSession or handle it however you like
    workout = WorkoutSession.objects.create(
        user=request.user,
        # other fields like duration_minutes, etc.
    )
    workout.exercises.set(selected_exercises)

    # ✅ Clear the selected exercises from the session to avoid duplication
    request.session['selected_exercises'] = []

    return redirect('dashboard')  # or wherever you show the workout


def workout_session(request):
    selected_exercises = request.session.get('selected_exercises', [])
    current_index = request.session.get('current_exercise_index', 0)

    if current_index >= len(selected_exercises):
        # Finished all exercises
        return redirect('workout_complete')

    # Get current exercise
    exercise_id = selected_exercises[current_index]
    exercise = Exercise.objects.get(id=exercise_id)

    return render(request, 'workout_session.html', {'exercise': exercise})

def mark_exercise_done(request):
    if request.method == 'POST':
        current_index = request.session.get('current_exercise_index', 0)
        request.session['current_exercise_index'] = current_index + 1
    return redirect('workout_session')

def workout_complete(request):
    # Optionally clear session or reset state here
    request.session.pop('current_exercise_index', None)
    return render(request, 'workout_complete.html')





from .models import Notification
from .forms  import NotificationForm                # ← now matches

from django.contrib.auth.decorators import login_required




from django.shortcuts import render, redirect
from .forms import NotificationForm


# workouts/views.py

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from .forms import NotificationForm
from .models import Notification

# workouts/views.py
from django.shortcuts import render
from datetime import datetime, timedelta
import pytz
from .tasks import send_scheduled_email  # Update import path if needed

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import pytz
from .tasks import send_scheduled_email  # adjust the import based on your project structure

@login_required
def schedule_email(request):
    user = request.user
    notify_email = getattr(user.profile, 'notify_email', '')

    if request.method == "POST":
        email = request.POST.get("email")
        time_str = request.POST.get("time")

        ph_tz = pytz.timezone("Asia/Manila")
        target_time = datetime.strptime(time_str, "%H:%M").time()
        now_ph = datetime.now(ph_tz)
        scheduled_datetime = datetime.combine(now_ph.date(), target_time)
        scheduled_datetime = ph_tz.localize(scheduled_datetime)

        if scheduled_datetime <= now_ph:
            scheduled_datetime += timedelta(days=1)

        send_scheduled_email.apply_async(args=[email], eta=scheduled_datetime)

        return render(request, "workouts/schedule_email.html", {
            "success": True,
            "prefill_email": email
        })

    return render(request, "workouts/schedule_email.html", {
        "prefill_email": notify_email
    })




















