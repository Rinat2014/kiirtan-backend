# users/serializers.py
import os
from rest_framework import serializers
from .models import User, UserLink #, LinkType, UserLink
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from django.urls import reverse
from django.db import models

from django.db import transaction
from django.utils.functional import empty


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
    
    'links',

}



# class UserLinkSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserLink
#         fields = ['id', 'name', 'url']
class UserLinkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = UserLink
        fields = ['id', 'name', 'url', 'public']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id","name"]


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


# 🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢
class UserSerializer(BaseUserSerializer):
    groups = GroupSerializer(many=True, read_only=True)  # для отдачи в API
    group_ids = serializers.PrimaryKeyRelatedField(      # для записи через PATCH/PUT
        many=True,
        queryset=Group.objects.all(),
        write_only=True,
        source="groups"
    )
    
    links = UserLinkSerializer(many=True, read_only=True)

    # Приём новых/обновлённых ссылок — мапим на тот же атрибут 'links'
    links_input = UserLinkSerializer(
        many=True,
        write_only=True,
        required=False,
        source='links'
    )
    
    
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

            # 'spirit_name',

            'utc_offset',
            'links_input',  # PUT, POST
            'links',        # GET

            'is_active',
            'is_staff',

            'group_ids',    # PUT, POST
            'groups',       # GET
        ]

        read_only_fields = ['id', 'email', 'groups']

    def update(self, instance, validated_data):
        """
        Основные идеи:
        - вытаскиваем links из validated_data сразу
        - применяем остальные поля к instance и сохраняем
        - затем обрабатываем links (создать/обновить/удалить)
        - корректно удаляем старый аватар, если загружен новый
        """
        print(f'validated_data === {validated_data}')

        # сначала достаём данные ссылок (они попадут сюда благодаря source='links')
        links_data = validated_data.pop('links', None)
        groups_data = validated_data.pop('groups', None)
        print(f'links_data: {links_data}')
        print(f'groups_data: {groups_data}')

        # avatar (если передаёте файл, он в validated_data как avatar_img)
        new_avatar = validated_data.get('avatar_img', None)
        old_avatar_path = None
        if new_avatar and instance.avatar_img:
            # запомним старый путь, удалим позже после успешного сохранения
            try:
                old_avatar_path = instance.avatar_img.path
            except Exception:
                old_avatar_path = None

        # применяем все остальные поля (оставшиеся в validated_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Обработка групп (роли пользователей)
        if groups_data is not None:
            instance.groups.set(groups_data)

        # удаляем старый файл аватара только после успешного сохранения нового
        if old_avatar_path and os.path.isfile(old_avatar_path):
            try:
                os.remove(old_avatar_path)
            except Exception:
                pass # логирование можно добавить, но не прерываем обновление
                

        # Обновляем/создаём/удаляем ссылки
        if links_data is not None:
            self._update_links(instance, links_data)

        return instance
    

    @staticmethod
    def _is_empty_url(val):
        """Считаем пустым: None или строка состоящая только из пробелов или пустая строка"""
        return val is None or (isinstance(val, str) and val.strip() == "")

    def _update_links(self, user, links_data):
        """
        links_data: список dict-ов, например:
        { "id": -12345, "name": "link", "url": "...", "public": False }
        Правила:
         - id > 0: ищем существующую ссылку у этого пользователя (update/delete)
         - id <= 0 или id отсутствует: считаем новой — создаём, если url не пустой
         - если для существующей ссылки ключ 'url' пришёл и он пустой — удаляем
         - обновляем только те поля, которые явно присутствуют в приходящем dict'е:
             -> 'url' (если непустой) / удалить если empty
             -> 'name'
             -> 'public'
        """
        # карта входные_ключи -> поля модели
        field_map = {
            'url': 'url',
            'name': 'name',
            'public': 'public',
            # при желании можно поддержать 'publick': 'public'
        }

        with transaction.atomic():
            for link_data in links_data:
                link_id = link_data.get('id', None)
                url_present = 'url' in link_data
                url_value = link_data.get('url', None) if url_present else None

                # Случай существующей сущности
                if link_id and isinstance(link_id, int) and link_id > 0:
                    try:
                        link = UserLink.objects.get(id=link_id, user=user)
                    except UserLink.DoesNotExist:
                        # id не найден — пропускаем
                        continue

                    # Удаляем ТОЛЬКО если ключ 'url' пришёл явно и url пустой
                    if url_present and self._is_empty_url(url_value):
                        link.delete()
                        continue

                    # Иначе — обновляем только те поля, которые явно пришли и разрешены
                    changed = False
                    for incoming_key, model_field in field_map.items():
                        if incoming_key not in link_data:
                            continue  # ключ не передан — ничего не трогаем

                        new_value = link_data[incoming_key]

                        # Для url: если пришёл непустой — обновляем; пустой handled выше
                        if model_field == 'url':
                            if self._is_empty_url(new_value):
                                # защищаемся — пропускаем обновление пустого url
                                continue
                            if getattr(link, 'url') != new_value:
                                setattr(link, 'url', new_value)
                                changed = True
                            continue

                        # Для остальных полей (name, public) — обновляем при отличии
                        current = getattr(link, model_field)
                        if current != new_value:
                            setattr(link, model_field, new_value)
                            changed = True

                    if changed:
                        link.save()

                else:
                    # Новая ссылка: создаём только если ключ 'url' присутствует и url непустой
                    if url_present and not self._is_empty_url(url_value):
                        create_data = {}
                        for incoming_key, model_field in field_map.items():
                            if incoming_key in link_data:
                                create_data[model_field] = link_data[incoming_key]

                        UserLink.objects.create(user=user, **create_data)
                    else:
                        # url отсутствует или пустой — не создаём
                        continue


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # def _is_empty_url(val):
    #     # Считаем пустым: None или строка состоящая только из пробелов или пустая строка
    #     if val is None:
    #         return True
    #     if isinstance(val, str) and val.strip() == "":
    #         return True
    #     return False

    # def _update_links(self, user, links_data):
    #     """
    #     links_data: список dict-ов, например:
    #     { "id": -12345, "name": "link", "url": "...", "public": False }
    #     Правила:
    #     - id > 0: ищем существующую ссылку у этого пользователя (update/delete)
    #     - id <= 0 или id отсутствует: считаем новой — создаём, если url не пустой
    #     - если для существующей ссылки ключ 'url' пришёл и он пустой — удаляем
    #     - обновляем только те поля, которые явно присутствуют в приходящем dict'е:
    #         -> 'url' (если непустой) / удалить если empty
    #         -> 'name'
    #         -> 'public' (поддерживается также входной ключ 'publick' — маппится на 'public')
    #     """
    #     # карта входные_ключи -> поля модели (защищает от попыток менять id/user и позволяет алиасы)
    #     field_map = {
    #         'url': 'url',
    #         'name': 'name',
    #         'public': 'public',
    #         # 'publick': 'public',  # поддержка опечатки/варианта
    #     }
    #     updatable_model_fields = set(field_map.values())

    #     with transaction.atomic():
    #         for link_data in links_data:
    #             link_id = link_data.get('id', None)
    #             # Берём url только если ключ присутствует (в дальнейшем проверяем пустоту)
    #             url_present = 'url' in link_data
    #             url_value = link_data.get('url', None) if url_present else None

    #             # Случай существующей сущности
    #             if link_id and isinstance(link_id, int) and link_id > 0:
    #                 try:
    #                     link = UserLink.objects.get(id=link_id, user=user)
    #                 except UserLink.DoesNotExist:
    #                     # id не найден — пропускаем
    #                     continue

    #                 # Удаляем ТОЛЬКО если ключ 'url' пришёл явно и url пустой
    #                 if url_present and self._is_empty_url(url_value):
    #                     link.delete()
    #                     continue

    #                 # Иначе — обновляем только те поля, которые явно пришли и разрешены
    #                 changed = False
    #                 for incoming_key, model_field in field_map.items():
    #                     if incoming_key not in link_data:
    #                         continue  # ключ не передан — ничего не трогаем

    #                     new_value = link_data[incoming_key]

    #                     # Для url: если пришёл непустой — обновляем; пустой handled выше
    #                     if model_field == 'url':
    #                         if self._is_empty_url(new_value):
    #                             # сюда мы не попадаем — т.к. пустой url мы уже удалили запись выше,
    #                             # но оставляем защиту: пропускаем обновление пустого url
    #                             continue
    #                         # Если url действительно отличается — обновляем
    #                         if getattr(link, 'url') != new_value:
    #                             setattr(link, 'url', new_value)
    #                             changed = True
    #                         continue

    #                     # Для остальных полей (name, public) — обновляем при отличии
    #                     current = getattr(link, model_field)
    #                     if current != new_value:
    #                         setattr(link, model_field, new_value)
    #                         changed = True

    #                 if changed:
    #                     link.save()

    #             else:
    #                 # Новая ссылка: создаём только если ключ 'url' присутствует и url непустой
    #                 if 'url' in link_data and not self._is_empty_url(link_data.get('url')):
    #                     # Собираем только разрешённые поля (и маппим publick->public)
    #                     create_data = {}
    #                     for incoming_key, model_field in field_map.items():
    #                         if incoming_key in link_data:
    #                             # url уже проверили на непустоту
    #                             create_data[model_field] = link_data[incoming_key]

    #                     # Если других полей нет — всё равно можно создать только с url
    #                     # (UserLink.objects.create ожидает user одним из обязательных полей)
    #                     UserLink.objects.create(user=user, **create_data)
    #                 else:
    #                     # url отсутствует или пустой — не создаём
    #                     continue






























    # def _update_links(self, user, links_data):
    #     """
    #     links_data: список dict-ов с полями, например:
    #     { "id": -12345, "name": "link", "url": "...", "public": False }
    #     Правила:
    #      - id > 0: ищем существующую ссылку у этого пользователя (update/delete)
    #      - id <= 0 или id отсутствует: считаем новой — создаём, если url не пустой
    #      - если для существующей ссылки url пустой — удаляем
    #     """
        
        
        
    #     for link_data in links_data:
    #         link_id = link_data.get('id', None)
    #         url = link_data.get('url', None)

    #         # существует положительный id — пробуем обновить/удалить
    #         if link_id and isinstance(link_id, int) and link_id > 0:
    #             try:
    #                 link = UserLink.objects.get(id=link_id, user=user)
    #             except UserLink.DoesNotExist:
    #                 # если id не найден — пропускаем или логируем
    #                 continue

    #             if not url:  # пустой url => удаляем сущность
    #                 link.delete()
    #             else:
    #                 # обновляем поля (без id и user)
    #                 for attr, value in link_data.items():
    #                     if attr in ('id', 'user'):
    #                         continue
    #                     setattr(link, attr, value)
    #                 link.save()

    #         else:
    #             # новые ссылки: если есть url — создаём
    #             if url:
    #                 # не передаём id и user (user заполним явно)
    #                 create_data = {k: v for k, v in link_data.items() if k not in ('id', 'user')}
    #                 UserLink.objects.create(user=user, **create_data)
    #             # если url пустой и id отрицательный — ничего не делаем
        
        
        
        
        
        # for link_data in links_data:
        #     link_id = link_data.get('id', None)
        #     url = link_data.get('url', None)

        #     # существует положительный id — пробуем обновить/удалить
        #     if link_id and isinstance(link_id, int) and link_id > 0:
        #         try:
        #             link = UserLink.objects.get(id=link_id, user=user)
        #         except UserLink.DoesNotExist:
        #             # если id не найден — пропускаем или логируем
        #             continue

        #         if not url:  # пустой url => удаляем сущность
        #             link.delete()
        #         else:
        #             # обновляем поля (без id и user)
        #             for attr, value in link_data.items():
        #                 if attr in ('id', 'user'):
        #                     continue
        #                 setattr(link, attr, value)
        #             link.save()

        #     else:
        #         # новые ссылки: если есть url — создаём
        #         if url:
        #             # не передаём id и user (user заполним явно)
        #             create_data = {k: v for k, v in link_data.items() if k not in ('id', 'user')}
        #             UserLink.objects.create(user=user, **create_data)
        #         # если url пустой и id отрицательный — ничего не делаем




















































    # def update(self, instance, validated_data):

    #     print(f'validated_data: {validated_data}')

    #     # сначала достаём данные ссылок (они попадут сюда благодаря source='links')
    #     links_data = validated_data.pop('links', None)

    #     # обновляем только переданные поля пользователя
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
        
        
    #     # avatar
    #     avatar = validated_data.get("avatar_img", None)

    #     # если загружаем новый аватар -> удаляем старый файл
    #     if avatar and instance.avatar_img:
    #         old_path = instance.avatar_img.path
    #         if os.path.isfile(old_path):
    #             os.remove(old_path)

    #     # Links
    #     print(f'update links ==================================================     00')
    #     links_data = validated_data.pop('links', None)

    #     print(f'links_data: {links_data}')
    #     print(f'validated_data: {validated_data}')

        
    #     if links_data is not None:
    #         self._update_links(instance, links_data)

    #     print(f'update links ==================================================     99')
    #     return instance

    #     # return super().update(instance, validated_data)

    # def _update_links(self, user, links_data):
    #     """
    #     Обновление списка ссылок:
    #     - если есть id и ссылка существует → обновляем
    #     - если есть id и url пустой → удаляем
    #     - если id нет → создаём новую
    #     """
    #     print(f'update links ==================================================     11')
    #     for link_data in links_data:
    #         link_id = link_data.get('id', None)
    #         url = link_data.get('url', None)

    #         print(f'id: {link_id} - {url}')

    #         if link_id:
    #             try:
    #                 link = UserLink.objects.get(id=link_id, user=user)
    #             except UserLink.DoesNotExist:
    #                 continue  # пропускаем несуществующие id

    #             if not url:  # если url пустой — удаляем
    #                 print(f'del - {link}')
    #                 link.delete()
    #             else:
    #                 for attr, value in link_data.items():
    #                     setattr(link, attr, value)
    #                 print(f'update link - {link}')
    #                 link.save()

    #         else:
    #             if url:  # создаём новую, если url не пустой
    #                 print(f'add link 🟢')
    #                 UserLink.objects.create(user=user, **link_data)





# 🟢🟡🔴
class MusicianListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

# 🟢🟡🔴
class ModeratorMusicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            # 'email', 
            # 'is_moderator_musicians'
        ]

# 🟢🟡🔴
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

# 🟢🟡🔴
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



# 🟢🟡🔴
class UserMeSerializer(serializers.ModelSerializer):
    
    links = UserLinkSerializer(many=True, read_only=True)

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
            
            'links',
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



# 🔴
class CustomTokenCreateSerializer(TokenCreateSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        
        # Просто обновляем поле
        self.user.last_login = timezone.now()
        self.user.save(update_fields=['last_login'])

        print(f"==================================================================================================  LOGIN")
        
        return attrs