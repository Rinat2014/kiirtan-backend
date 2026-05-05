# users/view.py

from .models import User

from .serializers import (
    ALLOWED_FIELDS,
    # RegisterSerializer,
    UserSerializer,
    UserMeSerializer,
    MusicianListSerializer,
    ModeratorMusicianSerializer,
    FullUserSerializer,
    UserInfoSerializer,
    # UserInfoUpdateSerializer,
    )
# from .serializers import 

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

from rest_framework import status, generics, exceptions
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied



ALLOWED_ROLE_FIELDS = [
    'is_musician',
    'is_editor',
    'is_moderator_musicians',
    'is_admin',
]



class UserMeView(APIView):
    # permission_classes = [IsAuthenticated]

    # def get(self, request):
    #     serializer = UserMeSerializer(request.user)
    #     return Response(serializer.data)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    


# from rest_framework.exceptions import PermissionDenied

class MusiciansListView(generics.ListAPIView):
    serializer_class = MusicianListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            User.objects.filter(groups__name="Musicians", is_active=True)
            .distinct()
            .order_by("username")
        )
    



class ModeratorMusiciansListView(generics.ListAPIView):
    serializer_class = ModeratorMusicianSerializer
    permission_classes = [IsAuthenticated]  # или IsAdminUser, если нужно ограничить доступ

    def get_queryset(self):
        return (
            User.objects.filter(groups__name="Moderators", is_active=True)
            .distinct()
            .order_by("username")
        )





class AllActiveUsersView(generics.ListAPIView):
    serializer_class = FullUserSerializer
    permission_classes = [IsAuthenticated]

    def check_permissions(self, request):
        super().check_permissions(request)
        user = request.user
        if not (
            # user.is_moderator_musicians or
            # user.is_moderator_site or
            # user.is_admin or
            user.is_staff or
            user.is_superuser
        ):
            raise PermissionDenied({
                "success": False,
                "message": "Доступ разрешен только модераторам и администраторам",
                "required_roles": {
                    "is_moderator_musicians": True,
                    "is_moderator_site": True,
                    "is_admin": True,
                    "is_staff": True,
                    "is_superuser": True
                },
                "your_roles": {
                    # "is_moderator_musicians": user.is_moderator_musicians,
                    # "is_moderator_site": user.is_moderator_site,
                    # "is_admin": user.is_admin,
                    "is_staff": user.is_staff,
                    "is_superuser": user.is_superuser
                }
            })

    def get_queryset(self):
        return User.objects.filter(is_active=True).order_by('username')





# class UserInfoView(generics.ListAPIView):
class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user_id = request.query_params.get('id')
        user = get_object_or_404(User, id=user_id)
        serializer = UserInfoSerializer(user)
        return Response(serializer.data)


User = get_user_model()


# 🔴🟠🟡🟢
class UserInfoUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        data = request.data

        print('UserInfoUpdateView           00          data= ', data)

        if not data or len(data) != 1:
            return Response({'detail': 'PUT request must contain exactly one field to update.'}, status=400)

        field_name, value = list(data.items())[0]

        if field_name not in ALLOWED_FIELDS:
            return Response({'detail': f'Field "{field_name}" is not allowed to be updated.'}, status=400)

        print('UserInfoUpdateView           11          ')
        # print('UserInfoUpdateView           11          ', field_name, ' --- ', value, '---             user=       ', user)

        setattr(user, field_name, value)
        user.save()


        # print('UserInfoUpdateView           22          ', field_name, ' --- ', value)
        
        


        
        return Response({'success': True, 'field_name': field_name, 'link': value}, status=status.HTTP_200_OK)
    
        

        # if serializer.is_valid():
        #     serializer.save()
        #     return Response({field_name: serializer.validated_data[field_name]}, status=200)
        # else:
        #     return Response(serializer.errors, status=400)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response({field_name: serializer.validated_data[field_name]}, status=200)
        # else:
        #     return Response(serializer.errors, status=400)



class UserRoleUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        current_user = request.user
        data = request.data

        # --- Проверка прав ---
        if not (current_user.is_moderator_musicians or current_user.is_admin):
            raise exceptions.PermissionDenied(
                "You don't have permission to change user roles."
            )

        user_id = data.get("user_id")
        field_name = data.get("field")
        value = data.get("value")

        if not user_id or not field_name:
            return Response(
                {"detail": "user_id and field are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ############################################################################## 
        if field_name not in ALLOWED_ROLE_FIELDS:
            return Response(
                {"detail": f'Field "{field_name}" is not a role field.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": f"User with id={user_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        setattr(user, field_name, bool(value))
        user.save()

        return Response(
            {
                "success": True,
                "user_id": user.id,
                "field": field_name,
                "new_value": getattr(user, field_name),
            },
            status=status.HTTP_200_OK,
        )