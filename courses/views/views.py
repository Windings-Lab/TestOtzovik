from django.contrib.auth.decorators import login_required
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden)
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView, ListView

from courses.forms import ReviewForm
from courses.linkedin import share_on_linkedin
from courses.models import Course, Review


class CourseListView(ListView):
    model = Course
    template_name = 'courses.html'
    context_object_name = 'courses'
    paginate_by = 1

    def get_queryset(self):
        return Course.objects.all()


class CourseDetailView(DetailView):
    def get(self, request, pk):
        course = Course.objects.get(pk=pk)
        approved_reviews = Review.objects.filter(course=course, status='approved')
        return render(request, 'course_detail.html', {'course': course, 'approved_reviews': approved_reviews})


class AddReviewView(View):
    template_name = 'add_review.html'

    def get(self, request, pk):
        form = ReviewForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        if form.is_valid():
            course = Course.objects.get(pk=pk)
            text = form.cleaned_data['text']
            rating = form.cleaned_data['rating']
            author = request.user
            existing_review = Review.objects.filter(author=author, course=course).exists()
            if existing_review:
                return HttpResponseForbidden("You have already left a review for this course.")
            Review.objects.create(author=author, text=text, rating=rating, course=course, status='pending')
            return redirect('course_detail', pk=pk)
        else:
            return render(request, self.template_name, {'form': form})


@login_required
def review_moderation(request):
    if not request.user.is_staff:
        return redirect('home')

    pending_reviews = Review.objects.filter(status=Review.PENDING)
    return render(request, 'review_moderation.html', {'pending_reviews': pending_reviews})


class ModerateReviewView(View):
    def post(self, request, review_id):
        try:
            review = Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            return HttpResponseBadRequest("Review does not exist")

        status = request.POST.get('status')

        if status not in ['approved', 'rejected']:
            return HttpResponseBadRequest("Invalid moderation status")

        if status == 'approved':
            review.status = 'approved'
            share_on_linkedin(
                access_token=review.author.get_access_token(),
                linkedin_id=review.author.linkedin_id,
                course_name=review.course.title
            )
            review.save()
            return HttpResponse("Review approved successfully")
        elif status == 'rejected':
            review.status = 'rejected'
            review.delete()
            return HttpResponse("Review rejected successfully")
