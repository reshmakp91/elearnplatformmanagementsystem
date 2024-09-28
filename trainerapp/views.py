from django.shortcuts import render, redirect, get_object_or_404
from managerapp.models import Course,Trainer,Order,Student
from trainerapp.models import Video, VideoProgress, Rating
from managerapp.forms import TrainerForm, CourseForm
from trainerapp.forms import VideoForm
from accountsapp.urls import urlpatterns
from django.db.models import Q

def dashboard(request):
    trainer_id = request.session.get('trainer_id')
    if not trainer_id:
        return redirect('login')
    courses = Course.objects.all()
    total_courses = Course.objects.count()
    total_trainers = Trainer.objects.count()
    context = {'courses': courses,'total_courses': total_courses,'total_trainers': total_trainers}
    return render(request,'trainer/dashboard.html',context)

def detailview(request, pk):
    trainer_id = request.session.get('trainer_id')
    if not trainer_id:
        return redirect('login')
    course = get_object_or_404(Course, pk=pk)
    videos = Video.objects.filter(course=course)
    context = {'course': course, 'videos': videos}
    return render(request, 'trainer/details.html', context)

def all_trainers(request):
    trainer_id = request.session.get('trainer_id')
    if not trainer_id:
        return redirect('login')
    trainers = Trainer.objects.all()
    context = {'trainers': trainers}
    return render(request, 'trainer/trainers.html', context)

def my_courses(request):
    trainer_id = request.session.get('trainer_id')
    if not trainer_id:
        return redirect('login')
    trainer = get_object_or_404(Trainer, id=trainer_id)
    my_courses = Course.objects.filter(trainer=trainer)
    context = {'my_courses': my_courses, 'trainer': trainer}
    return render(request, 'trainer/my_courses.html', context)

def my_profile(request):
    trainer_id = request.session.get('trainer_id')
    if not trainer_id:
        return redirect('login')
    trainer = get_object_or_404(Trainer, id=trainer_id)
    my_courses = Course.objects.filter(trainer=trainer)
    context = {'my_courses': my_courses, 'trainer': trainer}
    return render(request, 'trainer/my_profile.html', context)


def add_video(request):
    trainer_id = request.session.get('trainer_id')
    if not trainer_id:
        return redirect('login')
    trainer = Trainer.objects.get(id=trainer_id)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.trainer = trainer
            video.save()
            return redirect('my_courses')
    else:
        form = VideoForm()
    form.fields['course'].queryset = Course.objects.filter(trainer=trainer)
    return render(request, 'trainer/add_video.html', {'form': form})

def delete_video(request,video_id):
    trainer_id = request.session.get('trainer_id')
    if not trainer_id:
        return redirect('login')
    video = get_object_or_404(Video, id=video_id)
    course_id = video.course.id
    video.delete()
    return redirect('detailview_t', pk=course_id)

def logout(request):
    request.session.flush()
    return redirect('login')

def Search(request):
    trainer_id = request.session.get('trainer_id')
    if not trainer_id:
        return redirect('login')
    query = None
    courses = Course.objects.none()
    if 'q' in request.GET:
        query = request.GET.get('q')
        courses = Course.objects.filter(Q(title__icontains=query) | Q(trainer__name__icontains=query))
    context = {'courses': courses , 'query': query}
    return render(request, 'trainer/search.html', context)

def my_students(request):
    trainer_id = request.session.get('trainer_id')
    if not trainer_id:
        return redirect('login')
    trainer = get_object_or_404(Trainer, id=trainer_id)
    my_courses = Course.objects.filter(trainer=trainer)
    students_courses = []
    for course in my_courses:
        course_orders = Order.objects.filter(course=course)
        for order in course_orders:
            student = order.student
            videos = Video.objects.filter(course=course).order_by('id')
            total_videos = videos.count()
            watched_videos = VideoProgress.objects.filter(student=student, video__in=videos, watched=True).count()
            progress_percentage = (watched_videos / total_videos) * 100 if total_videos > 0 else 0
            try:
                rating = Rating.objects.get(student=student, course=course)
            except Rating.DoesNotExist:
                rating = None
            if (student, course) not in students_courses:
                students_courses.append((student, course, progress_percentage,rating))
    context = { 'trainer': trainer,'students_courses': students_courses, 'my_courses': my_courses}
    return render(request, 'trainer/view_students.html', context)


def student_profile(request,student_id):
    trainer_id = request.session.get('trainer_id')
    if not trainer_id:
        return redirect('login')
    student = get_object_or_404(Student, id=student_id)
    my_courses = Order.objects.filter(student=student)
    context = {'student': student, 'my_courses': my_courses}
    return render(request, 'trainer/student_profile.html', context)




