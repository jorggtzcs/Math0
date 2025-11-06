from django.urls import path
from django.contrib.auth import views as auth_views
from .import views

urlpatterns=[
#home page
path('',views.dashboard,name='dashboard'),

#Lesson List Page
path('lessons/',views.lesson_list,name='lesson_list'),

#Authentication URLS
path('login/',auth_views.LoginView.as_view(template_name='algebrai/login.html'),name='login'),
path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),

path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
path('lessons/<int:lesson_id>/grade/', views.grade_lesson, name='grade_lesson'),
path('lessons/<int:lesson_id>/results/', views.lesson_results, name='lesson_results'),
]