# users/serializers.py
import os
from rest_framework import serializers
from .models import User, UserLink #, LinkType, UserLink
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from django.urls import reverse
from django.db import models


from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from djoser.serializers import TokenCreateSerializer



User = get_user_model()


ALLOWED_FIELDS = {
    'username',
    'first_name',
    'last_name',
    'avatar_img',
    'user_info',

    # 'email',
    'utc_offset',
    'spirit_name',
    
    'social_bereal',
    'social_clubhouse',
    'social_discord',
    'social_douyin',
    'social_facebook',
    'social_instagram',
    'social_kakaotalk',
    'social_kuaishou',
    'social_line',
    'social_linkedin',
    'social_ok',
    'social_pinterest',
    'social_qq',
    'social_reddit',
    'social_snapchat',
    'social_telegram',
    'social_threads',
    'social_tiktok',
    'social_tumblr',
    'social_vkontakte',
    'social_wechat',
    'social_weibo',
    'social_whatsapp',
    'social_x',
    'social_youtube',  
}



class UserLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLink
        fields = ['id', 'name', 'url']





class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id","name")


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = BaseUserCreateSerializer.Meta.fields
        # fields = [
        #     "id",
        #     "email",
        #     "password",
        #     "re_password",
        #     "username",
        #     'utc_offset',
        # ]

    # def create(self, validated_data):
    #     user = super().create(validated_data)
    #     # user = User.objects.create_user(validated_data)

    #     # добавляем в группу "Musicians"
    #     musicians_group, _ = Group.objects.get_or_create(name="Musicians")
    #     user.groups.add(musicians_group)
    #     user.save()

    #     return user

        # fields = [
        #     'id',
        #     'email',
        #     'username',
        #     'first_name',
        #     'last_name',
        #     'spirit_name',
        #     'avatar_img',
        #     'user_info',

        #     'social_bereal',
        #     'social_clubhouse',
        #     'social_discord',
        #     'social_douyin',
        #     'social_facebook',
        #     'social_instagram',
        #     'social_kakaotalk',
        #     'social_kuaishou',
        #     'social_line',
        #     'social_linkedin',
        #     'social_ok',
        #     'social_pinterest',
        #     'social_qq',
        #     'social_reddit',
        #     'social_snapchat',
        #     'social_telegram',
        #     'social_threads',
        #     'social_tiktok',
        #     'social_tumblr',
        #     'social_vkontakte',
        #     'social_wechat',
        #     'social_weibo',
        #     'social_whatsapp',
        #     'social_x',
        #     'social_youtube',
        #     'spirit_name',

        #     'utc_offset',

        #     'is_musician',
        #     'is_moderator_musicians',
        #     'is_editor',
        #     'is_moderator_site',
        #     'is_admin',
        #     'is_active',
        #     'is_superuser',
        #     'is_staff',
        # ]


# 🟢
class UserSerializer(BaseUserSerializer):
    groups = GroupSerializer(many=True, read_only=True)  # для отдачи в API
    group_ids = serializers.PrimaryKeyRelatedField(      # для записи через PATCH/PUT
        many=True,
        queryset=Group.objects.all(),
        write_only=True,
        source="groups"
    )
    
    links = UserLinkSerializer(many=True, read_only=True)
    
    
    class Meta(BaseUserSerializer.Meta):
        model = User
        # fields = '__all__'
        # fields = BaseUserSerializer.Meta.fields + ('avatar_img', 'spirit_name', 'user_info', 'utc_offset', 'links')
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'spirit_name',
            'avatar_img',
            'user_info',

            'spirit_name',

            'utc_offset',
            'links', # 🟡

            'is_active',
            'is_staff',

            "groups",
            "group_ids",
        ]

    def update(self, instance, validated_data):
        avatar = validated_data.get("avatar_img", None)

        # если загружаем новый аватар -> удаляем старый файл
        if avatar and instance.avatar_img:
            old_path = instance.avatar_img.path
            if os.path.isfile(old_path):
                os.remove(old_path)

        return super().update(instance, validated_data)


    # class RegisterSerializer(serializers.ModelSerializer):
    #     password2 = serializers.CharField(write_only=True)

    #     # class Meta:
    #     #     model = User
    #     #     fields = ['email', 'username', 'password', 'password2', 'utc_offset']
    #     #     extra_kwargs = {'password': {'write_only': True}}

    #     # def validate(self, attrs):
            
    #     #     print(f"\nПолученные данные:\n", attrs) 
            
    #     #     if attrs['password'] != attrs['password2']:
    #     #         raise serializers.ValidationError({"password": "The passwords do not match"}) # Пароли не совпадают
            
    #     #     # data = super().validate(attrs)
    #     #     # data['username'] = attrs['username']  # Добавляем username в ответ
    #     #     # return data
    #     #     return attrs

    #     # def create(self, validated_data):
    #     #     validated_data.pop('password2')
    #     #     user = User.objects.create_user(**validated_data, is_active=False)
            
    #     #     print(f'\ncreate user ============================================================ \n{user}')

    #     #     # Отправляем письмо для подтверждения email
    #     #     # current_site = get_current_site(self.context['request'])         # {current_site.domain}
    #     #     # current_site = 'localhost:8000'
    #     #     verification_link = f"http://localhost:3000/activate/{user.id}/"   # prod
    #     #     # verification_link = f"http://localhost:3000/activate/{user.id}/"
    #     #     # verification_link = f"http://{current_site}/api/users/activate/{user.id}/"
    #     #     # http://localhost:3000/activate/23/
    #     #     print(f'verification_link= {verification_link}\n============================================================')
            
    #     #     # на время тестирования отключаем
    #     #     send_mail(
    #     #         'Подтвердите ваш email',
    #     #         f'Пройдите по ссылке для активации аккаунта: {verification_link}',
    #     #         'site-akhanda-kirtan@yandex.ru',
    #     #         [user.email],
    #     #         fail_silently=False,
    #     #     )
    #     #     return user



class MusicianListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
        ]

class ModeratorMusicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            # 'email', 
            # 'is_moderator_musicians'
        ]

class FullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'spirit_name',
            'avatar_img',
            'user_info',

            'social_bereal',
            'social_clubhouse',
            'social_discord',
            'social_douyin',
            'social_facebook',
            'social_instagram',
            'social_kakaotalk',
            'social_kuaishou',
            'social_line',
            'social_linkedin',
            'social_ok',
            'social_pinterest',
            'social_qq',
            'social_reddit',
            'social_snapchat',
            'social_telegram',
            'social_threads',
            'social_tiktok',
            'social_tumblr',
            'social_vkontakte',
            'social_wechat',
            'social_weibo',
            'social_whatsapp',
            'social_x',
            'social_youtube',
            'spirit_name',

            'utc_offset',

            'is_musician',
            'is_moderator_musicians',
            'is_editor',
            'is_moderator_site',
            'is_admin',
            'is_active',
            'is_superuser',
            'is_staff',
        ]

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'spirit_name',
            'avatar_img',
            'user_info',

            # 'social_bereal',
            # 'social_clubhouse',
            # 'social_discord',
            # 'social_douyin',
            # 'social_facebook',
            # 'social_instagram',
            # 'social_kakaotalk',
            # 'social_kuaishou',
            # 'social_line',
            # 'social_linkedin',
            # 'social_ok',
            # 'social_pinterest',
            # 'social_qq',
            # 'social_reddit',
            # 'social_snapchat',
            # 'social_telegram',
            # 'social_threads',
            # 'social_tiktok',
            # 'social_tumblr',
            # 'social_vkontakte',
            # 'social_wechat',
            # 'social_weibo',
            # 'social_whatsapp',
            # 'social_x',
            # 'social_youtube',
            # 'spirit_name',

            'utc_offset',

            # 'is_musician',
            # 'is_moderator_musicians',
            # 'is_editor',
            # 'is_moderator_site',
            # 'is_admin',
            'is_active',
            'is_superuser',
            'is_staff',
        ]

    # class UserInfoUpdateSerializer(serializers.ModelSerializer):
    #     class Meta:
    #         model = User
    #         fields = []  # динамически задаём в `__init__`

    #         def __init__(self, *args, **kwargs):
    #             # field = kwargs.pop('field', None)
                
    #             # self.update_field = kwargs.pop('field', None)
    #             super().__init__(*args, **kwargs)

    #             update_field = self.context.get('field')  # ✅ Получаем из context

    #             # if field and field in [f.name for f in User._meta.fields]:
    #             #     # self.fields[field] = self.Meta.model._meta.get_field(field).formfield().widget.attrs.get('max_length', 255)
    #             #     self.fields[field] = serializers.CharField(allow_blank=True, required=False)
    #             # else:
    #             #     raise serializers.ValidationError({"detail": "Invalid field"})

    #             if update_field not in ALLOWED_FIELDS:
    #                 raise serializers.ValidationError({'detail': f'Invalid field: {update_field}'})

    #             model_field = User._meta.get_field(update_field)

    #             # # Определим нужный тип сериализатора по типу поля модели
    #             # if isinstance(model_field, models.BooleanField):
    #             #     self.fields[self.update_field] = serializers.BooleanField(required=True)
    #             # elif isinstance(model_field, models.IntegerField):
    #             #     self.fields[self.update_field] = serializers.IntegerField(required=True)
    #             # else:
    #             #     self.fields[self.update_field] = serializers.CharField(
    #             #         allow_blank=True, required=True, max_length=255
    #             #     )
    #             # Тип поля → тип сериализатора
    #             if isinstance(model_field, models.BooleanField):
    #                 self.fields[update_field] = serializers.BooleanField(required=True)
    #             elif isinstance(model_field, models.IntegerField):
    #                 self.fields[update_field] = serializers.IntegerField(required=True)
    #             else:
    #                 self.fields[update_field] = serializers.CharField(
    #                     allow_blank=True,
    #                     required=True,
    #                     max_length=255
    #                 )



# 🔴
class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'is_active',
            
            'is_musician',
            'is_editor',
            'is_admin',
            'is_moderator_musicians',
            'is_moderator_site',
        ]




    # class Meta(BaseUserSerializer.Meta):
    #     model = User
    #     # fields = '__all__'
    #     # fields = BaseUserSerializer.Meta.fields + ('avatar_img', 'spirit_name', 'user_info', 'utc_offset', 'links')
    #     fields = [
    #         'id',
    #         'email',
    #         'username',
    #         'first_name',
    #         'last_name',
    #         'spirit_name',
    #         'avatar_img',
    #         'user_info',

    #         # 'social_bereal',
    #         # 'social_clubhouse',
    #         # 'social_discord',
    #         # 'social_douyin',
    #         # 'social_facebook',
    #         # 'social_instagram',
    #         # 'social_kakaotalk',
    #         # 'social_kuaishou',
    #         # 'social_line',
    #         # 'social_linkedin',
    #         # 'social_ok',
    #         # 'social_pinterest',
    #         # 'social_qq',
    #         # 'social_reddit',
    #         # 'social_snapchat',
    #         # 'social_telegram',
    #         # 'social_threads',
    #         # 'social_tiktok',
    #         # 'social_tumblr',
    #         # 'social_vkontakte',
    #         # 'social_wechat',
    #         # 'social_weibo',
    #         # 'social_whatsapp',
    #         # 'social_x',
    #         # 'social_youtube',
    #         'spirit_name',

    #         'utc_offset',
    #         'links', # 🟡

    #         # 'is_musician',
    #         # 'is_moderator_musicians',
    #         # 'is_editor',
    #         # 'is_moderator_site',
    #         # 'is_admin',
    #         # 'is_superuser',
            
    #         'is_active',
    #         'is_staff',

    #         "groups",
    #         "group_ids",
    #     ]

    
    
    
class CustomTokenCreateSerializer(TokenCreateSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        
        # Просто обновляем поле
        self.user.last_login = timezone.now()
        self.user.save(update_fields=['last_login'])
        
        return attrs