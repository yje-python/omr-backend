# omr/serializers.py

from rest_framework import serializers
from .models import Exam, Answer, WrongNote


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class ExamSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = '__all__'


class WrongNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = WrongNote
        fields = '__all__'