
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Course, Enrollment, Question, Choice, Submission


def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Get the learner's enrollment
    enrollment = get_object_or_404(
        Enrollment,
        course=course,
        user=request.user
    )

    # Get all questions related to the course
    questions = Question.objects.filter(course=course)

    if request.method == 'POST':

        selected_choices = []

        # Collect the selected choices
        for question in questions:
            selected_id = request.POST.get(
                f'question_{question.id}'
            )

            if selected_id:
                choice = get_object_or_404(
                    Choice,
                    id=selected_id,
                    question=question
                )
                selected_choices.append(choice)

        # Create one submission for this exam
        submission = Submission.objects.create(
            enrollment=enrollment
        )

        # Attach selected choices to the submission
        submission.choices.set(selected_choices)

        # Redirect to the exam result page
        return redirect(
            'show_exam_result',
            course_id=course.id,
            submission_id=submission.id
        )

    return redirect('course_details', course_id=course.id)


def show_exam_result(request, course_id, submission_id):

    course = get_object_or_404(Course, id=course_id)

    enrollment = get_object_or_404(
        Enrollment,
        course=course,
        user=request.user
    )

    submission = get_object_or_404(
        Submission,
        id=submission_id,
        enrollment=enrollment
    )

    # Get selected choice IDs
    selected_ids = list(
        submission.choices.values_list('id', flat=True)
    )

    # Calculate the total grade
    questions = Question.objects.filter(course=course)

    grade = sum(
        question.is_get_score(selected_ids)
        for question in questions
    )

    context = {
        'course': course,
        'submission': submission,
        'questions': questions,
        'selected_ids': selected_ids,
        'grade': grade,
    }

    return render(
        request,
        'onlinecourse/exam_result_bootstrap.html',
        context
    )

