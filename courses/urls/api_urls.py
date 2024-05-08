from django.urls import path

from courses.views.api_views import CourseDetailApiView, CoursesListApiView, ReviewDetailApiView, ApprovedReviewsApiView

urlpatterns = [
    path('courses/', CoursesListApiView.as_view(), name='api_courses_detail'),
    path('courses/<int:pk>', CourseDetailApiView.as_view(), name='api_course_detail'),
    path('reviews/<int:pk>', ReviewDetailApiView.as_view(), name='api_review_detail'),
    path('courses/reviews/<int:course_id>', ApprovedReviewsApiView.as_view(), name='api_approved_reviews_for_course')
]
