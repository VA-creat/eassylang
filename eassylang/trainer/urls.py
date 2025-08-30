from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('words/', views.word_list, name='word_list'),
    path('words/add/', views.word_add, name='word_add'),
    path('lessons/', views.lesson_list, name='lesson_list'),
    path('lessons/add/', views.lesson_add, name='lesson_add'),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('import/', views.import_csv, name='import_csv'),
    path('practice/start/', views.practice_start, name='practice_start'),
    path('practice/<uuid:session_id>/run/', views.practice_run, name='practice_run'),
    path('practice/<uuid:session_id>/result/', views.practice_result, name='practice_result'),
]
