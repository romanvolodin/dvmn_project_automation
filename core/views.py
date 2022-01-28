import json

from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.db import transaction
from django.http import JsonResponse

from .models import Student
from .models import StudentProjectPreferences
from .serializers import StudentSerializer


@api_view(['GET'])
def get_students_preferences(request):
    dumped_prefs = []
    prefs = StudentProjectPreferences.objects.all()

    for pref in prefs:
        dumped_pref = {
            "student": pref.student.name,
            "project": pref.project.title,
        }
        dumped_prefs.append(dumped_pref)

    return JsonResponse(
        dumped_prefs,
        safe=False,
        json_dumps_params={
            'ensure_ascii': False,
            'indent': 4,
            }
        )


@api_view(['POST'])
def add_student(request):
    serializer = StudentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True) 
    
    tg_chat_id = serializer.validated_data.pop('tg_chat_id')

    student, _ = Student.objects.update_or_create(
        tg_chat_id=tg_chat_id,
        defaults=serializer.validated_data
        )
    serializer = StudentSerializer(student)
   
    return Response(serializer.data)
