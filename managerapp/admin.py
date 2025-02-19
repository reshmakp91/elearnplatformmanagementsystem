from django.contrib import admin
from .models import Course, Trainer, Student, Country, State, District, manager, Payment
from trainerapp.models import Rating

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'trainer', 'price')

class TrainerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'username', 'password', 'country', 'state', 'district')


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')

class ManagerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','username','password')

class RatingAdmin(admin.ModelAdmin):
    list_display = ('student','course','trainer','rating','review')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course','amount', 'stripe_payment_id','status','created_at')


admin.site.register(Course, CourseAdmin)
admin.site.register(Trainer, TrainerAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(manager, ManagerAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Payment, PaymentAdmin)

