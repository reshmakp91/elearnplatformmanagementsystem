from django.shortcuts import render, redirect, get_object_or_404
from managerapp.models import Course,Trainer,Student, Cart, CartItem, Order, Payment
from trainerapp.models import Video, VideoProgress, Rating
from managerapp.forms import TrainerForm, CourseForm, RatingForm
from trainerapp.forms import VideoForm
from accountsapp.urls import urlpatterns
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
import stripe

def dashboard(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    courses = Course.objects.all()
    total_courses = Course.objects.count()
    context = {'courses': courses,'total_courses': total_courses}
    return render(request,'student/dashboard.html',context)

def detailview(request, pk):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    course = get_object_or_404(Course, pk=pk)
    student = get_object_or_404(Student, id=student_id)
    has_purchased = Order.objects.filter(student=student, course=course).exists()
    if not has_purchased:
        messages.warning(request, 'You need to purchase this course to access its videos.')
        return redirect('student_dashboard')
    videos = Video.objects.filter(course=course).order_by('id')
    total_videos = videos.count()
    watched_videos = VideoProgress.objects.filter(student=student, video__in=videos, watched=True).values_list('video_id', flat=True)
    watched_count = len(watched_videos)
    progress_percentage = (watched_count / total_videos) * 100 if total_videos > 0 else 0
    next_video = None
    for video in videos:
        if video.id not in watched_videos:
            next_video = video
            break
    context = {'course': course,'videos': videos,'watched_videos': watched_videos,'next_video': next_video,'progress_percentage': progress_percentage}
    return render(request, 'student/details.html', context)

def mark_video_as_watched(request, video_id):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    video = get_object_or_404(Video, id=video_id)
    student = get_object_or_404(Student, id=student_id)
    progress, created = VideoProgress.objects.get_or_create(student=student, video=video)
    progress.watched = True
    progress.save()
    return redirect('play_video', video_id=video.id)

def play_video(request, video_id):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    video = get_object_or_404(Video, id=video_id)
    context = {'video': video}
    return render(request, 'student/play_video.html', context)

def faq(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    return render(request, 'student/faq.html')

def contact_view(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    return render(request, 'student/contact.html')

def my_profile(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    student = get_object_or_404(Student, id=student_id)
    my_courses = Order.objects.filter(student=student)
    context = {'student': student,'my_courses': my_courses}
    return render(request, 'student/my_profile.html', context)

def logout(request):
    request.session.flush()
    return redirect('login')

def Search(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    query = None
    courses = Course.objects.none()
    if 'q' in request.GET:
        query = request.GET.get('q')
        courses = Course.objects.filter(Q(title__icontains=query) | Q(trainer__name__icontains=query))
    context = {'courses': courses , 'query': query}
    return render(request, 'student/search.html', context)

def view_cart(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    student = Student.objects.get(username=request.session['username'])
    cart, created = Cart.objects.get_or_create(student=student)
    cart_items = cart.cartitem_set.all()
    total_items = cart_items.count()
    total_price = sum(item.course.price for item in cart_items)
    context = {'cart_items': cart_items, 'total_price': total_price, 'total_items': total_items}
    return render(request, 'student/cart.html', context)

def add_to_cart(request,course_id):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    c = Course.objects.get(id=course_id)
    student = Student.objects.get(username=request.session['username'])
    cart, created = Cart.objects.get_or_create(student=student)
    cart_item,item_created = CartItem.objects.get_or_create(cart=cart,course=c)
    if not item_created:
        cart_item.save()
    return redirect('viewcart')

def remove_from_cart(request, item_id):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    try:
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.delete()
        messages.success(request, 'Item removed from cart.')
    except CartItem.DoesNotExist:
        messages.error(request, 'Cart item not found.')
    return redirect('viewcart')

def create_checkout_session(request):

    if request.method == 'POST':
        student = Student.objects.get(username=request.session['username'])
        cart, created = Cart.objects.get_or_create(student=student)
        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items.exists():
            messages.warning(request, 'No items in cart.')
            return redirect('viewcart')
        stripe.api_key = settings.STRIPE_SECRET_KEY
        lineitems = []
        for cart_item in cart_items:
            if cart_item.course and cart_item.course.price > 0:
                lineitem = {
                    'price_data': {
                        'currency': 'INR',
                        'unit_amount': int(cart_item.course.price * 100),
                        'product_data': {
                            'name': cart_item.course.title,
                        },
                    },
                    'quantity': 1,
                }
                lineitems.append(lineitem)
        if lineitems:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=lineitems,
                mode='payment',
                success_url=request.build_absolute_uri(reverse('success')),
                cancel_url=request.build_absolute_uri(reverse('cancel'))
            )
            for cart_item in cart_items:
                Payment.objects.create(
                    student=student,
                    course=cart_item.course,
                    amount=cart_item.course.price,
                    stripe_payment_id=checkout_session.id,
                    status='pending'
                )
            return redirect(checkout_session.url, code=303)
    return redirect('viewcart')

def success(request):
    student = Student.objects.get(username=request.session['username'])
    cart_items = CartItem.objects.filter(cart__student=student)
    for cart_item in cart_items:
        Order.objects.create(student=student, course=cart_item.course)
        Payment.objects.filter(student=student, course=cart_item.course).update(status='paid')
        product = cart_item.course
        product.save()
    cart_items.delete()
    return render(request,'student/success.html')

def cancel(request):
    return render(request, 'student/cancel.html')

def my_orders(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    student = Student.objects.get(username=request.session['username'])
    orders = Order.objects.filter(student=student).order_by('-order_date')
    context = {'orders': orders}
    return render(request, 'student/my_orders.html', context)

def give_rating(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    student = Student.objects.get(username=request.session['username'])
    orders = Order.objects.filter(student=student)
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course = Course.objects.get(id=course_id)
        trainer = course.trainer
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.student = student
            rating.course = course
            rating.trainer = trainer
            rating.save()
            messages.success(request, 'Thank you for rating the course!')
            return redirect('my_orders')
        else:
            messages.error(request, 'There was an error with your rating. Please try again.')
    context = {'orders': orders,'rating_form': RatingForm()}
    return render(request, 'student/give_rating.html', context)

def trainer_support(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    student = Student.objects.get(username=request.session['username'])
    orders = Order.objects.filter(student=student)
    trainer = None
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        try:
            course = Course.objects.get(id=course_id)
            order = orders.filter(course=course)
            if order and course.trainer:
                trainer = course.trainer
            else:
                messages.error('No trainer assigned or you haven’t purchased this course.')
        except Course.DoesNotExist:
            messages.error('No courses found')
    context = {'orders': orders,'trainer':trainer}
    return render(request, 'student/trainer_support.html', context)
