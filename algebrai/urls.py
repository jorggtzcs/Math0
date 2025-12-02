from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView

urlpatterns = [
    # home page
    path('', views.dashboard, name='dashboard'),

    # Lesson List Page
    path('lessons/', views.lesson_list, name='lesson_list'),

    # Authentication URLS
    path('signup/', views.signup, name='signup'),
    # path('login/',auth_views.LoginView.as_view(template_name='algebrai/login.html'),name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lessons/<int:lesson_id>/grade/', views.grade_lesson, name='grade_lesson'),
    path('lessons/<int:lesson_id>/results/', views.lesson_results, name='lesson_results'),
   # path('lessons/create/', views.create_lesson, name='create_lesson'),
   # path('lessons/<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'),
    #path('lessons/<int:lesson)id>/add-exercise/', views.add_exercise, name='add_exercise'),
    path('classes/', views.class_list, name='class_list'),
    path('classes/create/', views.class_create, name='class_create'),
    path('classes/<int:class_id>/', views.class_detail, name='class_detail'),
    path('classes/<int:class_id>/student<int:student_id>/', views.class_student_detail, name='class_student_detail'),
    path('classes/join/', views.class_join, name='class_join'),
]
