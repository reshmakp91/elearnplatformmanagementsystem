from django.db import models
from django.conf import settings

class Trainer(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField()
    username = models.CharField(max_length=100,null=True)
    password = models.CharField(max_length=100,null=True)
    type = models.CharField(max_length=100,null=True)
    skype_id = models.CharField(max_length=100,null=True)
    whatsapp = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.name

class Course(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='course_images/', default='default_image.jpg')
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.IntegerField(default=0)
    def __str__(self):
        return self.title

class Student(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, null=True, unique=True)
    password = models.CharField(max_length=128,null=True)
    type = models.CharField(max_length=100, null=True)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey('State', on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey('District', on_delete=models.SET_NULL, null=True)
    def set_password(self, raw_password):
        self.password = raw_password
    def __str__(self):
        return self.username

class manager(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, null=True, unique=True)
    password = models.CharField(max_length=128, null=True)
    type = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, related_name='states', on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, related_name='districts', on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Cart(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    items = models.ManyToManyField(Course)

class CartItem(models.Model):
    student = models.ForeignKey(Student, null=True, blank=True, on_delete=models.SET_NULL)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    course =  models.ForeignKey(Course, on_delete=models.CASCADE)

class Order(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_id = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.title} - {self.amount}"



