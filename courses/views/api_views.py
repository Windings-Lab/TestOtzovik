from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course, Review
from courses.serializers import CourseSerializer, ReviewSerializer, ApprovedReviewSerializer


class CoursesListApiView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetailApiView(APIView):
    def get(self, request, pk):
        course = Course.objects.get(pk=pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)


class ReviewDetailApiView(APIView):
    def get(self, request, pk):
        review = Review.objects.get(pk=pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)


class ApprovedReviewsApiView(APIView):
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        approved_review = Review.objects.filter(course=course, status='approved')
        serializer = ApprovedReviewSerializer(approved_review, many=True)
        return Response(serializer.data)


