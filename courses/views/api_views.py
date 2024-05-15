from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.linkedin import share_on_linkedin
from courses.models import Course, Review
from courses.serializers import (ApprovedReviewSerializer, CourseSerializer,
                                 ReviewFormSerializer,
                                 ReviewModerationSerializer, ReviewSerializer)


class IsStaffPermission(BasePermission):
    """ Allows access only to staff users. """

    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class CoursesListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @swagger_auto_schema(
        operation_summary="List all courses",
        operation_description="Retrieve a list of all courses."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CourseDetailAPIView(APIView):
    @swagger_auto_schema(
        responses={200: CourseSerializer()},
        operation_summary='Retrieve a single course by ID',
        operation_description='Retrieve details of a specific course by ID.'
    )
    def get(self, request, pk):
        course = Course.objects.get(pk=pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)


class CourseSearchAPIView(ListAPIView):
    serializer_class = CourseSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="A search term.", type=openapi.TYPE_STRING,
                              format='string'),
        ],
        operation_summary='Search courses by title',
        operation_description='Retrieve courses whose title contains the specified string.'
    )
    def get_queryset(self):
        title = self.request.query_params.get('search', '')
        return Course.objects.filter(title__icontains=title)


# class CourseSearchAPIView(APIView):
#     serializer_class = CourseSerializer
#
#     @swagger_auto_schema(
#         manual_parameters=[
#             openapi.Parameter('search', openapi.IN_QUERY, description="A search term.", type=openapi.TYPE_STRING),
#         ],
#         operation_summary='Search courses by title',
#         operation_description='Retrieve courses whose title contains the specified string.'
#     )
#     def get(self, request, *args, **kwargs):
#         search_term = request.query_params.get('search', '')
#
#         if search_term:
#             courses = Course.objects.filter(title__icontains=search_term)
#         else:
#             courses = Course.objects.all()
#
#         serializer = self.serializer_class(courses, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewDetailAPIView(APIView):
    @swagger_auto_schema(
        responses={200: ReviewSerializer()},
        operation_summary='Retrieve a single review by ID',
        operation_description='Retrieve details of a specific review by ID.'
    )
    def get(self, request, pk):
        review = Review.objects.get(pk=pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)


class ApprovedReviewsAPIView(APIView):
    @swagger_auto_schema(
        responses={200: ReviewSerializer()},
        operation_summary='Retrieve a list of approved reviews by COURSE ID',
        operation_description='Retrieve details of a approved reviews by COURSE ID.'
    )
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        approved_review = Review.objects.filter(course=course, status='approved')
        serializer = ApprovedReviewSerializer(approved_review, many=True)
        return Response(serializer.data)


class AddReviewAPIView(APIView):
    serializer_class = ReviewFormSerializer

    @swagger_auto_schema(
        request_body=ReviewFormSerializer,
        operation_summary="Add a review for a course",
        operation_description="Add a review for a course identified by its ID.",
        responses={201: "Created", 400: "Bad Request", 403: "Forbidden"}
    )
    def post(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            course = Course.objects.get(pk=pk)
            text = serializer.validated_data['text']
            rating = serializer.validated_data['rating']
            author = request.user
            existing_review = Review.objects.filter(course=course, author=author).exists()
            if existing_review:
                return Response({"detail": "You have already left a review for this course."},
                                status=status.HTTP_403_FORBIDDEN)
            Review.objects.create(author=author, text=text, course=course, rating=rating, status='pending')
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewModerationAPIView(APIView):
    permission_classes = [IsAuthenticated, IsStaffPermission]

    @swagger_auto_schema(
        operation_summary="List pending reviews for moderation",
        operation_description="Retrieve a list of pending reviews that require moderation.",
        responses={200: openapi.Response("List of pending reviews", ReviewSerializer(many=True))}
    )
    def get(self, request):
        pending_reviews = Review.objects.filter(status=Review.PENDING)
        serializer = ReviewSerializer(pending_reviews, many=True)
        return Response(serializer.data)


class ModerateReviewAPIView(APIView):
    @swagger_auto_schema(
        request_body=ReviewModerationSerializer,
        operation_summary="Moderate a review",
        operation_description="Update the status of a review (approve/reject).",
        responses={200: "Review status updated successfully", 400: "Bad Request"}
    )
    def patch(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({"detail": "Review does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReviewModerationSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            if 'status' in serializer.validated_data:
                status_value = serializer.validated_data['status']
                if status_value == 'approved':
                    review.status = 'approved'
                    share_on_linkedin(
                        access_token=review.author.get_access_token(),
                        linkedin_id=review.author.linkedin_id,
                        course_name=review.course.title
                    )
                    review.save()
                elif status_value == 'rejected':
                    review.status = 'rejected'
                    review.delete()
                return Response({"detail": f"Review {status_value} successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Status field is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


