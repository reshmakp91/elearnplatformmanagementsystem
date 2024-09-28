from django.db import models
from managerapp.models import Trainer, Course, Student
from django.core.validators import MinValueValidator, MaxValueValidator

class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='course_videos/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class VideoProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
    watch_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.video.title} - Watched: {self.watched}"

class Rating(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.student.username} rated {self.course.title} with {self.rating} stars"


