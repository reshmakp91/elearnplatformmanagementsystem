from django.shortcuts import render, redirect
from managerapp.models import Trainer,Student, manager
from django.contrib import messages
from managerapp.forms import TrainerForm, StudentRegistrationForm

def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']
        if role == 'trainer':
            try:
                user = Trainer.objects.get(username=username)
                if user.password == password:
                    request.session['trainer_id'] = user.id
                    request.session['username'] = user.username
                    return redirect('trainer_dashboard')
                else:
                    messages.error(request, 'Invalid password for Trainer.')
            except Trainer.DoesNotExist:
                messages.error(request, 'Invalid username for Trainer.')
        elif role == 'student':
            try:
                user = Student.objects.get(username=username)
                if user.password == password:
                    request.session['student_id'] = user.id
                    request.session['username'] = user.username
                    return redirect('student_dashboard')
                else:
                    messages.error(request, 'Invalid password for Student.')
            except Student.DoesNotExist:
                messages.error(request, 'Invalid username for Student.')
        elif role == 'manager':
            try:
                user = manager.objects.get(username=username)
                if user.password == password:
                    request.session['manager_id'] = user.id
                    request.session['username'] = user.username
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid password for Manager.')
            except Student.DoesNotExist:
                messages.error(request, 'Invalid username for Manager.')
    return render(request, 'accounts/login.html')

def student_register(request):
    form = StudentRegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            student = form.save(commit=False)
            student.type = 'student'
            student.set_password(form.cleaned_data["password"])
            student.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')
    else:
        if 'country' in request.GET:
            country_id = request.GET.get('country')
            form.fields['state'].queryset = State.objects.filter(country_id=country_id)
        if 'state' in request.GET:
            state_id = request.GET.get('state')
            form.fields['district'].queryset = District.objects.filter(state_id=state_id)
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

def contact(request):
    return render(request, 'accounts/Contact.html')



