from rest_framework import serializers

from courses.models import Course, Review


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'price', 'company', 'group', 'location', 'website', 'contact', 'description']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'course', 'status']


class ApprovedReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'course', 'status']
