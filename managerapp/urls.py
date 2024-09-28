from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-course/', views.add_course, name='add_course'),
    path('add-trainer/', views.add_trainer, name='add_trainer'),
    path('allot-trainer/<int:course_id>/', views.allot_trainer, name='allot_trainer'),
    path('course/<int:pk>/', views.detailview, name='detailview'),
    path('course/<int:pk>/delete/', views.deleteview, name='deleteview'),
    path('course/<int:pk>/update/', views.updateview, name='update'),
    path('trainers/', views.all_trainers, name='trainer_details'),
    path('trainer/<int:trainer_id>/edit/', views.edit_trainer, name='edit_trainer'),
    path('trainer/<int:trainer_id>/delete/', views.delete_trainer, name='delete_trainer'),
    path('course/<int:pk>/remove_trainer/', views.remove_trainer, name='remove_trainer'),
    path('search/', views.Search, name='search'),
    path('students/',views.all_students,name='student_details'),
    path('logout/',views.logout,name='logout'),
    path('student-profile/<int:student_id>/',views.student_profile,name='student_profile_m'),
    path('student/<int:student_id>/delete/', views.delete_student, name='delete_student'),
    path('trainer_feedback/<int:trainer_id>/',views.trainer_feedback,name='trainer_feedback'),
    path('payment_details/<int:student_id>/',views.payment_details,name='payment_details'),
    path('update_payment/<int:payment_id>/', views.update_paydetails, name='update_payment_details'),
]
