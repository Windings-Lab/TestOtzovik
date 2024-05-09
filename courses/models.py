from django.db import models
from django.db.models import Avg

from users.models import CustomUser


class Course(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    company = models.CharField(max_length=255)
    group = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    website = models.URLField()
    contact = models.CharField(max_length=255)
    description = models.TextField()
    time_added = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

    @property
    def review_counter(self):
        approved_reviews = Review.objects.filter(status='approved')
        return approved_reviews.count()

    def average_rating(self):
        approved_reviews = Review.objects.filter(status='approved')
        return approved_reviews.aggregate(Avg('rating'))['rating__avg']


class Review(models.Model):
    text = models.TextField()
    rating = models.IntegerField(choices=[
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ])
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews_written')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    MODERATION_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=MODERATION_CHOICES, default=PENDING)
    time_added = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}, Review for {self.course.title} by {self.author.full_name}"
