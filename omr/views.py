# omr/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Exam, WrongNote
from .serializers import ExamSerializer, WrongNoteSerializer


@api_view(['GET'])
def exam_list(request):
    exams = Exam.objects.all().order_by('-created_at')
    return Response(ExamSerializer(exams, many=True).data)


@api_view(['POST'])
def create_exam(request):
    serializer = ExamSerializer(data=request.data)
    if serializer.is_valid():
        exam = serializer.save()
        return Response(ExamSerializer(exam).data)
    return Response(serializer.errors)


@api_view(['GET'])
def wrong_notes(request, exam_id):
    notes = WrongNote.objects.filter(exam_id=exam_id)
    return Response(WrongNoteSerializer(notes, many=True).data)