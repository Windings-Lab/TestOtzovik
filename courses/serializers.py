from rest_framework import serializers

from courses.models import Course, Review


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'price', 'company', 'age', 'location', 'website', 'contact', 'description']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'course', 'status']


class ApprovedReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'course', 'status']


class ReviewFormSerializer(serializers.Serializer):
    text = serializers.CharField()
    rating = serializers.IntegerField(min_value=1, max_value=5)


class ReviewModerationSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Review.MODERATION_CHOICES)

    class Meta:
        model = Review
        fields = ['status']
