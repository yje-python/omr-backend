from django.contrib import admin
from django.urls import path
from omr import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Exam
    path('api/exams/', views.exam_list),         # GET, POST 같이 처리
    path('api/exams/<int:exam_id>/', views.exam_detail),

    # WrongNote
    path('api/wrong-notes/', views.create_wrong_note),
    path('api/wrong-notes/<int:exam_id>/', views.wrong_notes),
    path('api/wrong-notes/update/<int:note_id>/', views.update_wrong_note),
    path('api/tags/', views.tag_list),
    path('api/wrong-note-tags/', views.update_wrongnote_tags),
    path('api/exams/wrong/', views.exams_with_wrong_notes),
    path('api/tags/<int:tag_id>/', views.delete_tag),
    path('api/wrong-notes/delete/<int:exam_id>/', views.delete_wrong_notes_by_exam),
]