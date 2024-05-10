from django.urls import path

from courses.views.views import (AddReviewView, CourseDetailView,
                                 CourseListView, ModerateReviewView,
                                 review_moderation)

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('course/<int:pk>/add-review/', AddReviewView.as_view(), name='add-review'),
    path('review_moder', review_moderation, name='review_moder'),
    path('moderate_review/<int:review_id>/', ModerateReviewView.as_view(), name='moderate-review'),
]
