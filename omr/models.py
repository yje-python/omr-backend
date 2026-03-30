# omr/models.py

from django.db import models


class Exam(models.Model):
    exam_name = models.CharField(max_length=100)
    template_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Subject(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='subjects')

    subject_name = models.CharField(max_length=100)
    question_count = models.IntegerField()
    time_limit = models.IntegerField()


class Answer(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='answers')

    question_number = models.IntegerField()
    user_answer = models.IntegerField(null=True)
    correct_answer = models.IntegerField()

    is_correct = models.BooleanField()


class WrongNote(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='wrong_notes')

    question_number = models.IntegerField()

    user_answer = models.IntegerField()
    correct_answer = models.IntegerField()

    memo = models.TextField(blank=True)


class Tag(models.Model):
    name = models.CharField(max_length=50)


class WrongNoteTag(models.Model):
    wrong_note = models.ForeignKey(WrongNote, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)