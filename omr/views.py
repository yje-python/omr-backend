# omr/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Exam, Subject, Answer, WrongNote, Tag, WrongNoteTag
from .serializers import ExamSerializer, WrongNoteSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Count
import time

import time

import time

@api_view(['GET', 'POST'])
def exam_list(request):

    if request.method == 'GET':
        exams = Exam.objects.all().order_by('-created_at')
        return Response(ExamSerializer(exams, many=True).data)

    elif request.method == 'POST':
        data = request.data

        exam = Exam.objects.create(
            exam_name=data.get('exam_name'),
            template_id=data.get('template_id')
        )

        subjects = data.get('subjects', [])

        for subject_data in subjects:
            subject = Subject.objects.create(
                exam=exam,
                subject_name=subject_data.get('subject_name'),
                question_count=subject_data.get('question_count'),
                time_limit=subject_data.get('time_limit'),
            )

            answers = subject_data.get('answers', [])
            correct_answers = subject_data.get('correct_answers', [])

            answer_objs = []
            wrongnote_objs = []

            for i in range(len(answers)):
                user = answers[i]
                correct = correct_answers[i] if i < len(correct_answers) else None
                is_correct = (user == correct) if correct is not None else False

                answer_objs.append(
                    Answer(
                        subject=subject,
                        question_number=i + 1,
                        user_answer=user,
                        correct_answer=correct,
                        is_correct=is_correct
                    )
                )

                if user is not None and not is_correct:
                    wrongnote_objs.append(
                        WrongNote(
                            subject=subject,
                            question_number=i + 1,
                            user_answer=user,
                            correct_answer=correct,
                            memo=''
                        )
                    )

            Answer.objects.bulk_create(answer_objs)

            if wrongnote_objs:
                WrongNote.objects.bulk_create(wrongnote_objs)

        start = time.time()

        res = ExamSerializer(exam).data

        print("⏱ serialize time:", time.time() - start)

        return Response(res)


@api_view(['GET', 'DELETE'])
def exam_detail(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == 'GET':
        return Response(ExamSerializer(exam).data)

    elif request.method == 'DELETE':
        exam.delete()
        return Response({'message': 'deleted'})


@api_view(['GET'])
def wrong_notes(request, exam_id):
    notes = WrongNote.objects.filter(subject__exam_id=exam_id)
    return Response(WrongNoteSerializer(notes, many=True).data)

@api_view(['POST'])
def create_wrong_note(request):
    data = request.data

    wrong_note = WrongNote.objects.create(
        subject_id=data.get('subject_id'),
        question_number=data.get('question_number'),
        user_answer=data.get('user_answer'),
        correct_answer=data.get('correct_answer'),
        memo=data.get('memo', '')
    )

    return Response({
        'id': wrong_note.id,
        'message': 'created'
    })

@api_view(['PATCH'])
def update_wrong_note(request, note_id):
    note = get_object_or_404(WrongNote, id=note_id)

    note.memo = request.data.get('memo', note.memo)
    note.save()

    return Response({'message': 'updated'})

@api_view(['GET', 'POST'])
def tag_list(request):
    if request.method == 'GET':
        tags = Tag.objects.all()
        return Response([{'id': t.id, 'name': t.name} for t in tags])

    elif request.method == 'POST':
        tag = Tag.objects.create(name=request.data.get('name'))
        return Response({'id': tag.id, 'name': tag.name})
    
@api_view(['POST'])
def update_wrongnote_tags(request):
    note_id = request.data.get('wrong_note')
    tag_ids = request.data.get('tags', [])

    note = get_object_or_404(WrongNote, id=note_id)

    WrongNoteTag.objects.filter(wrong_note=note).delete()

    for tag_id in tag_ids:
        WrongNoteTag.objects.create(
            wrong_note=note,
            tag_id=tag_id
        )

    return Response({'message': 'updated'})

@api_view(['GET'])
def exams_with_wrong_notes(request):
    exams = Exam.objects.filter(
        subjects__wrong_notes__isnull=False
    ).distinct().order_by('-created_at')

    return Response(ExamSerializer(exams, many=True).data)

@api_view(['DELETE'])
def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    tag.delete()
    return Response({'message': 'deleted'})

@api_view(['DELETE'])
def delete_wrong_notes_by_exam(request, exam_id):
    notes = WrongNote.objects.filter(subject__exam_id=exam_id)
    notes.delete()
    return Response({'message': 'deleted'})