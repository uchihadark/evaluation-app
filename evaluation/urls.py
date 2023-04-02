from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('view_students/<int:mentor_id>/', views.view_students, name='view_students'),
    path('students/<int:student_id>/edit/', views.edit_student, name='edit_student'),
    path('students/<int:student_id>/delete/', views.delete_student, name='delete_student'),
    path('mentor/<int:mentor_id>/submit_final_marks/', views.submit_final_marks, name='submit_final_marks'),
]