import random
import string

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from .forms import ClassroomForm
from .models import Lesson, Exercise, Option, StudentProgress, Profile, Classroom
from django.contrib import messages

# Create your views here.
'''
@login_required
def dashboard(request):
    lessons=Lesson.objects.all()
    student=request.user

    completed_count=StudentProgress.objects.filter(student=student,completed=True).count()
    correct_count=StudentProgress.objects.filter(student=student,is_correct=True).count()
    return render(request, 'algebrai/dashboard.html', {
        'lessons':lessons,
        'completed_count':completed_count,
        'correct_count':correct_count
    })
'''


@login_required
def dashboard(request):
    lessons = Lesson.objects.all()
    student = request.user

    lesson_progress = []
    for lesson in lessons:
        exercises = lesson.exercises.all()
        completed_count = StudentProgress.objects.filter(
            student=student,
            exercise__in=exercises,
            completed=True
        ).count()
        exercises = lesson.exercises.all()
        correct_count = StudentProgress.objects.filter(
            student=student,
            exercise__in=exercises,
            is_correct=True
        ).count()
        total_exercises = exercises.count()

        lesson_progress.append({
            'lesson': lesson,
            'complete': completed_count,
            'correct_count': correct_count,
            'total': total_exercises
        })
    return render(request, 'algebrai/dashboard.html', {'lesson_progress': lesson_progress})


@login_required
def lesson_list(request):
    lessons = Lesson.objects.all()
    return render(request, 'algebrai/lesson_list.html', {'lessons': lessons})


@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)  # get lesson or return 400 error
    exercises = lesson.exercises.all()
    return render(request, 'algebrai/lesson_detail.html', {'lesson': lesson, 'exercises': exercises})


@login_required
def grade_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    exercises = Exercise.objects.filter(lesson=lesson)

    results = []
    score = 0

    for exercise in exercises:
        selected_option_id = request.POST.get(f'exercise_{exercise.id}')

        if selected_option_id:
            selected_option = Option.objects.get(id=selected_option_id)
            is_correct = selected_option.is_correct
            if is_correct:
                score += 1

            progress, created = StudentProgress.objects.update_or_create(
                student=request.user, exercise=exercise,
                defaults={
                    'selected_option': selected_option,
                    'completed': True,
                    'is_correct': is_correct
                }
            )
        else:
            selected_option = None
            is_correct = False

        results.append({
            'exercise': exercise,
            'selected_option': selected_option,
            'is_correct': is_correct,
        })
    total = exercises.count()

    request.session['grading_data'] = {
        'score': score,
        'total': total,
        'results': [
            {
                'question': r['exercise'].question_text,
                'selected': r['selected_option'].option_text if r['selected_option'] else None,
                'correct': r['is_correct'],
                'correct_answer': r['exercise'].options.filter(is_correct=True).first().option_text
            }
            for r in results
        ]
    }

    return redirect('lesson_results', lesson_id=lesson_id)


@login_required
def lesson_results(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    grading_data = request.session.get('grading_data')

    return render(request, 'algebrai/lesson_results.html', {
        'lesson': lesson,
        'score': grading_data['score'],
        'total': grading_data['total'],
        'results': grading_data['results'],
    })


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, is_teacher=False)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'algebrai/signup.html', {'form': form})


'''
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            messages.error(request, "User not found. Please sign up.")
            return redirect('signup')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Incorrect password.")
            # return render(request,"algebrai/login.html")

    return render(request, "algebrai/login.html")
'''


class CustomLoginView(LoginView):
    template_name = 'algebrai/login.html'

    def form_invalid(self, form):
        username = self.request.POST.get('username')
        if not User.objects.filter(username=username).exists():
            messages.info(self.request, 'User not found. Please sign up.')
            return redirect('signup')
        else:
            messages.error(self.request, "Incorrect password.")
            return super().form_invalid(form)

    def get_success_url(self):
        if hasattr(self.request.user, 'profile') and self.request.user.profile.is_teacher:
            return reverse_lazy('teacher_dashboard')
        return reverse_lazy('student_dashboard')


@login_required
def teacher_dashboard(request):
    if not request.user.profile.is_teacher:
        return redirect('dashboard')

    students = User.objects.filter(profile__is_teacher=False)
    progress = StudentProgress.objects.select_related('student', 'exercise')
    return render(request, 'algebrai/teacher_dashboard.html', {'students': students,
                                                               'progress': progress})


@login_required
def student_dashboard(request):
    return redirect('dashboard')


def _generate_class_code(length=6):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))


# list classes
@login_required
def class_list(request):
    user = request.user
    if hasattr(user, 'profile') and user.profile.is_teacher:
        classes = Classroom.objects.filter(teacher=user)
    else:
        classes = Classroom.objects.filter(enrollments__student=user)
    return render(request, 'algebrai/class_list.html', {'classes': classes})


# create class teacher
@login_required
def class_create(request):
    if not request.user.profile.is_teacher:
        messages.error(request, "Only teachers can create classes.")
        return redirect('class list')

    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            classroom = form.save(comit=False)
            classroom.teacher = request.user
            # generate a unique code
            code = _generate_class_code()
            while Classroom.objects.filter(code=code).exists():
                code = _generate_class_code()
            classroom.code = code
            classroom.save()
            messages.success(request, f"'{classroom.name}' create. Join code: {classroom.code}")
            return redirect('class_detail', class_id=classroom.id)
        else:
            form = ClassroomForm()
        return render(request, 'algebrai/class.create.html', {'form': form})
