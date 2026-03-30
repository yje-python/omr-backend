# omr/serializers.py

from rest_framework import serializers
from .models import Exam, Subject, Answer, WrongNote


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class WrongNoteSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = WrongNote
        fields = '__all__'

    def get_tags(self, obj):
        return list(
            obj.wrongnotetag_set.values_list('tag_id', flat=True)
        )

class SubjectSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    wrong_notes = WrongNoteSerializer(many=True, read_only=True)

    class Meta:
        model = Subject
        fields = '__all__'


class ExamSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = '__all__'


