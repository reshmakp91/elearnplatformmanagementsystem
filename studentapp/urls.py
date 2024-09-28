from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard,name='student_dashboard'),
    path('details/<int:pk>',views.detailview, name='details_s'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact_view,name='contact'),
    path('my_profile/',views.my_profile,name='my_profile'),
    path('search/', views.Search, name='search_student'),
    path('viewcart/',views.view_cart ,name='viewcart'),
    path('addtocart/<int:course_id>/',views.add_to_cart ,name='addtocart'),
    path('remove/<int:item_id>/',views.remove_from_cart,name='remove_cart'),
    path('create_checkout_session',views.create_checkout_session,name='create_checkout_session'),
    path('success/',views.success,name='success'),
    path('cancel/',views.cancel,name='cancel'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('video/<int:video_id>/watched/', views.mark_video_as_watched, name='mark_video_as_watched'),
    path('play_video/<int:video_id>/', views.play_video, name='play_video'),
    path('give_rating/',views.give_rating,name='give_rating'),
    path('trainer_support/',views.trainer_support,name='trainer_support')
]
