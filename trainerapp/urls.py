from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='trainer_dashboard'),
    path('coursedetail/<int:pk>/', views.detailview, name='detailview_t'),
    path('trainers/', views.all_trainers, name='trainer_details_t'),
    path('my_courses/', views.my_courses, name='my_courses'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('add_video/', views.add_video, name='add_video'),
    path('delete_video/<int:video_id>/', views.delete_video, name='delete_video'),
    path('logout/',views.logout,name='logout'),
    path('search/', views.Search, name='search_trainer'),
    path('my_students/', views.my_students, name='students_in_courses'),
    path('student/<int:student_id>/', views.student_profile, name='student_profile'),
]
