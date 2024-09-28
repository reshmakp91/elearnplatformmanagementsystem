from django.shortcuts import render, redirect, get_object_or_404
from managerapp.models import Course,Trainer,Student, Order, manager, Payment
from managerapp.forms import TrainerForm, CourseForm
from trainerapp.models import Video, VideoProgress, Rating
from django.db.models import Q
from django.contrib import messages

def dashboard(request):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login')
    courses = Course.objects.all()
    total_courses = Course.objects.count()
    total_trainers = Trainer.objects.count()
    context = {'courses': courses,'total_courses': total_courses,'total_trainers': total_trainers}
    return render(request,'manager/dashboard.html',context)

def add_course(request):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login')
    if request.method == 'POST':
        form = CourseForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CourseForm()
    return render(request, 'manager/add_course.html', {'form': form})

def add_trainer(request):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login')
    if request.method == 'POST':
        form = TrainerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TrainerForm()
    return render(request, 'manager/add_trainer.html', {'form': form})


def allot_trainer(request, course_id):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login')
    try:
        selected_course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return redirect('dashboard')
    trainers = Trainer.objects.all()
    if request.method == 'POST':
        trainer_id = request.POST.get('trainer')
        if trainer_id:
            try:
                trainer = Trainer.objects.get(id=trainer_id)
                selected_course.trainer = trainer
                selected_course.save()
                return redirect('dashboard')
            except Trainer.DoesNotExist:
                error = 'Invalid trainer selection. Please try again.'
        else:
            error = 'Please select a trainer.'
        return render(request, 'manager/allot_trainer.html', {'selected_course': selected_course,'trainers': trainers,'error': error })
    return render(request, 'manager/allot_trainer.html', {'selected_course': selected_course,'trainers': trainers})

def listCourse(request):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login')
    courses = Course.objects.all()
    return render(request,'manager/dashboard.html', {'Courses': courses})

def detailview(request,pk):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login')
    course = get_object_or_404(Course, pk=pk)
    videos = Video.objects.filter(course=course)
    context = {'course': course, 'videos': videos}
    return render(request, 'manager/details.html', context)

def deleteview(request, pk):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login')
    course = get_object_or_404(Course,pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('dashboard')
    return render(request, 'manager/delete.html', {'course': course})

def updateview(request, pk):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login')
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES,instance=course)
        if form.is_valid():
            form.save()
            return redirect('detailview', pk=pk)
    else:
        form = CourseForm(instance=course)
    context = {'form': form, 'course': course}
    return render(request, 'manager/update.html', context)

def all_trainers(request):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login')
    trainers = Trainer.objects.all()
    context = {'trainers': trainers}
    return render(request, 'manager/trainers.html', context)

def edit_trainer(request, trainer_id):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login')
    trainer = get_object_or_404(Trainer, id=trainer_id)
    if request.method == 'POST':
        form = TrainerForm(request.POST, instance=trainer)
        if form.is_valid():
            form.save()
            return redirect('trainer_details')
    else:
        form = TrainerForm(instance=trainer)
    return render(request, 'manager/edit_trainer.html', {'form': form, 'trainer': trainer})

def delete_trainer(request, trainer_id):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login')
    trainer = get_object_or_404(Trainer, id=trainer_id)
    if request.method == 'POST':
        trainer.delete()
        return redirect('trainer_details')
    return render(request, 'manager/delete_trainer.html', {'trainer': trainer})

def remove_trainer(request, pk):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login')
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.trainer = None
        course.save()
        return redirect('dashboard')
    return render(request, 'manager/remove.html', {'course': course})

def Search(request):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login')
    query = None
    courses = Course.objects.none()
    if 'q' in request.GET:
        query = request.GET.get('q')
        courses = Course.objects.filter(Q(title__icontains=query) | Q(trainer__name__icontains=query))
    context = {'courses': courses , 'query': query}
    return render(request, 'manager/search.html', context)

def all_students(request):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login')
    students = Student.objects.all()
    student_progress = []
    orders = []
    for student in students:
        orders = Order.objects.filter(student=student)
        for order in orders:
            course = order.course
            videos = Video.objects.filter(course=course)
            total_videos = videos.count()
            watched_videos = VideoProgress.objects.filter(student=student, video__in=videos, watched=True).count()
            progress_percentage = (watched_videos / total_videos) * 100 if total_videos > 0 else 0
            student_progress.append({'student': student,'course': course,'progress_percentage': progress_percentage})
    context = {'students': students, 'orders': orders, 'student_progress': student_progress}
    return render(request, 'manager/students.html', context)

def logout(request):
    request.session.flush()
    return redirect('login')

def student_profile(request,student_id):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login')
    student = get_object_or_404(Student, id=student_id)
    my_courses = Order.objects.filter(student=student)
    context = {'student': student, 'my_courses': my_courses}
    return render(request, 'manager/student_profile.html', context)

def delete_student(request, student_id):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login')
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('student_details')
    return render(request, 'manager/delete_student.html', {'student': student})

def trainer_feedback(request, trainer_id):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login')
    trainer = get_object_or_404(Trainer, id=trainer_id)
    try:
        rating = Rating.objects.filter(trainer=trainer)
    except Rating.DoesNotExist:
        rating = None
    context = {'trainer': trainer,'rating': rating}
    return render(request, 'manager/trainer_feedback.html', context)

def payment_details(request, student_id):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login')
    student = get_object_or_404(Student, id=student_id)
    pay_details = Payment.objects.filter(student=student)
    context = {'student': student,'pay_details': pay_details}
    return render(request,'manager/payment_details.html', context)

def update_paydetails(request, payment_id):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login')
    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == 'POST':
        payment.amount = request.POST.get('amount', payment.amount)
        payment.status = request.POST.get('status', payment.status)
        payment.save()
        messages.success(request, 'Payment details updated successfully.')
        return redirect('payment_details', student_id=payment.student.id)
    context = {'payment': payment}
    return render(request, 'manager/update_payment.html', context)









