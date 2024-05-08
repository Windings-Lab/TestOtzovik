from django.urls import path

from .views import (AddReviewView, CourseDetailView, CourseListView,
                    ModerateReviewView, review_moderation)

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('course/<int:pk>/add_review/', AddReviewView.as_view(), name='add_review'),
    path('review_moderation', review_moderation, name='review_moderation'),
    path('moderate_review/<int:review_id>/', ModerateReviewView.as_view(), name='moderate_review'),
]
