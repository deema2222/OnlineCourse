
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Course, Question, Choice, Submission


def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    questions = Question.objects.filter(course=course)

    score = 0
    total_questions = questions.count()

    for question in questions:
        selected_choice_id = request.POST.get(
            f"question_{question.id}"
        )

        if selected_choice_id:
            selected_choice = Choice.objects.filter(
                id=selected_choice_id,
                question=question
            ).first()

            if selected_choice:
                Submission.objects.create(
                    question=question,
                    selected_choice=selected_choice
                )

                if selected_choice.is_correct:
                    score += 1

    percentage = (
        (score / total_questions) * 100
        if total_questions > 0 else 0
    )

    request.session['exam_result'] = {
        'course_id': course.id,
        'course_name': course.name,
        'score': score,
        'total_questions': total_questions,
        'percentage': percentage,
    }

    return redirect(
        'show_exam_result',
        course_id=course.id
    )


def show_exam_result(request, course_id):
    result = request.session.get('exam_result')

    if not result or result['course_id'] != course_id:
        return redirect('course_details', course_id=course_id)

    context = {
        'course_name': result['course_name'],
        'score': result['score'],
        'total_questions': result['total_questions'],
        'percentage': result['percentage'],
    }

    return render(
        request,
        'onlinecourse/exam_result_bootstrap.html',
        context
    )
