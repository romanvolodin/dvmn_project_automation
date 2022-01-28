from rest_framework.serializers import ModelSerializer
from .models import Student


class StudentSerializer(ModelSerializer):

    class Meta:
        model = Student
        fields = [
            'name',
            'level',
            'tg_username',
            'tg_chat_id',
            'discord_username',
            'is_far_east',
            ]
