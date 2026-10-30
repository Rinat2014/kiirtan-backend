# musicians/serializers.py
from rest_framework import serializers
from .models import MusicSlot
from users.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class MusicSlotSerializer(serializers.ModelSerializer):
    musician = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    musician_obj = UserSerializer(source='musician', read_only=True)

    class Meta:
        model = MusicSlot
        fields = '__all__'
        # fields = ['id', 'musician', 'musician_detail', '...']

