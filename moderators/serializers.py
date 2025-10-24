# moderators/serializers.py
from rest_framework import serializers
from .models import ModeratorSlot
from users.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

# class ModeratorSlotSerializer(serializers.ModelSerializer):
#     moderator = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(), write_only=True
#     )
#     moderator_obj = UserSerializer(source='moderator', read_only=True)

#     class Meta:
#         model = ModeratorSlot
#         fields = '__all__'
#         # или явно: fields = ['id', 'musician', 'musician_detail', '...']




class ModeratorSlotSerializer(serializers.ModelSerializer):
    moderator = UserSerializer(read_only=True)
    moderator_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        source='moderator',
        write_only=True
    )

    class Meta:
        model = ModeratorSlot
        fields = '__all__'
        extra_kwargs = {
            'moderator': {'read_only': True},
        }