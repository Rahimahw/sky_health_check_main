from django.urls import path
from . import views

urlpatterns = [
    path('team-leader/progress/', views.team_leader_progress_report, name='team_leader_progress'),
    path('department-leader/progress/', views.department_leader_progress, name='department_leader_progress'),
    path('senior-manager/progress/', views.senior_manager_progress, name='senior_manager_progress'),
    path("not-authorised/", views.not_authorised, name="not_authorised"),


]
