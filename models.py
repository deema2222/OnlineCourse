
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=500)

    course = models.ForeignKey(
        'onlinecourse.Course',
        on_delete=models.CASCADE,
        related_name='questions'
    )

    grade = models.IntegerField(default=0)

    def is_get_score(self, selected_ids):
        correct_ids = set(
            self.choices.filter(is_correct=True)
            .values_list('id', flat=True)
        )
        selected_ids = set(selected_ids)

        return self.grade if correct_ids == selected_ids else 0

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices'
    )

    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(
        'onlinecourse.Enrollment',
        on_delete=models.CASCADE,
        related_name='submissions'
    )

    choices = models.ManyToManyField(
        Choice,
        related_name='submissions'
    )

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission for {self.enrollment}"

