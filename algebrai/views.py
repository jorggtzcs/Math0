from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Lesson, Exercise, Option

# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'algebrai/dashboard.html')

@login_required
def lesson_list(request):
    lessons=Lesson.objects.all()
    return render(request,'algebrai/lesson_list.html',{'lessons':lessons})

@login_required
def lesson_detail(request, lesson_id):
    lesson=get_object_or_404(Lesson, id=lesson_id) #get lesson or return 400 error
    exercises=lesson.exercises.all()
    return render(request, 'algebrai/lesson_detail.html', {'lesson':lesson, 'exercises': exercises})

@login_required
def grade_lesson(request, lesson_id):
    lesson=get_object_or_404(Lesson,id=lesson_id)
    exercises=Exercise.objects.filter(lesson=lesson)

    results=[]
    score=0

    for exercise in exercises:
        selected_option_id=request.POST.get(f'exercise_{exercise.id}')

        if selected_option_id:
            selected_option=Option.objects.get(id=selected_option_id)
            is_correct=selected_option.is_correct
            if is_correct:
                score+=1
        else:
            selected_option=None
            is_correct=False

        results.append({
            'exercise':exercise,
            'selected_option':selected_option,
            'is_correct': is_correct,
        })
    total=exercises.count()

    request.session['grading_data'] = {
        'score': score,
        'total': total,
        'results': [
            {
                'question': r['exercise'].question_text,
                'selected': r['selected_option'].text if r['selected_option'] else None,
                'correct': r['is_correct'],
                'correct_answer': r['exercise'].options.filter(is_correct=True).first().text
            }
            for r in results
        ]
    }

    return redirect('lesson_results', lesson_id=lesson_id)

@login_required
def lesson_results(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    grading_data= request.session.get('grading_data')

    return render(request, 'algebrai/lesson_results.html', {
        'lesson': lesson,
        'score': grading_data['score'],
        'total': grading_data['total'],
        'results': grading_data['results'],
    })



