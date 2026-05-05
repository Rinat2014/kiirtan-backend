# moderators/views.py
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import datetime, timedelta
from django.db.models.functions import ExtractWeekDay
from django.utils.timezone import now
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime, parse_date
from django_filters.rest_framework import DjangoFilterBackend

from .models import ModeratorSlot
from .serializers import ModeratorSlotSerializer
from .permissions import IsModeratorOrAdmin
from .filters import ModeratorSlotFilter



class ModeratorSlotViewSet(viewsets.ModelViewSet):
    queryset = ModeratorSlot.objects.all()  # Важно для DRF router
    serializer_class = ModeratorSlotSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ModeratorSlotFilter



    def get_queryset(self):
        queryset = super().get_queryset().order_by('time')
        query_params = self.request.query_params

        # Если в параметрах передан id — фильтруем только по id
        if 'id' in query_params:
            return queryset.filter(id=query_params['id'])

        # Если нет параметров вообще — фильтруем по дате
        if not query_params:
            today = now()
            end_date = today + timedelta(days=7)
            queryset = queryset.filter(time__date__gte=today.date() - timedelta(days=1), time__date__lte=end_date.date())

        return queryset




    # def get_permissions(self):
    #     if self.action == 'create':
    #         permission_classes = [IsModeratorOrAdmin]
    #     elif self.action in ['update', 'partial_update']:
    #         permission_classes = [IsModeratorOrAdmin]
    #     elif self.action == 'destroy':
    #         permission_classes = [IsModeratorOrAdmin]
    #     else:
    #         permission_classes = [permissions.AllowAny]
    #     return [perm() for perm in permission_classes]
    def get_permissions(self):
      permission_map = {
          'create': [IsModeratorOrAdmin],
          'update': [IsModeratorOrAdmin],
          'partial_update': [IsModeratorOrAdmin],
          'destroy': [IsModeratorOrAdmin],
      }
      permission_classes = permission_map.get(self.action, [permissions.AllowAny])
      return [perm() for perm in permission_classes]
    


    def create(self, request, *args, **kwargs):
        data = request.data
        is_regular = data.get('is_regular', False)
        times = data.get('time')
        user_id = data.get('moderator_id')
        
        print(f'create moderator ================================================================================ 1')
        print(f'data: {data}')
        print(f'create moderator ================================================================================ 2')

        # # Устанавливаем текущего пользователя как музыканта
        # data['moderator'] = request.user.id
        
        # устанавливаем пользователя на запись - id которого передается через SlotData.moderator
        # data['moderator'] = data.get('moderator')
        

        if is_regular:
            # Обработка множественной записи
            if isinstance(times, list):
                created_slots = []
                skipped_slots = []

                for time_str in times:
                    try:
                        time = make_aware(datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S"))
                    except ValueError:
                        skipped_slots.append(time_str)
                        continue  # Просто пропускаем
                        # return Response({"detail": f"Неверный формат времени: {time_str}"}, status=status.HTTP_400_BAD_REQUEST)

                    if ModeratorSlot.objects.filter(time=time).exists():
                        skipped_slots.append(time_str)
                        continue  # Просто пропускаем
                        # return Response({"detail": f"Таймслот {time_str} уже занят."}, status=status.HTTP_400_BAD_REQUEST)

                    slot_data = {
                        'time': time,
                        'is_regular': True,
                        'moderator_id': user_id
                    }

                    serializer = self.get_serializer(data=slot_data)
                    if serializer.is_valid():
                        created_slots.append(serializer.save())
                    # serializer.is_valid(raise_exception=True)
                    # created_slots.append(serializer.save())

                # Возвращаем созданные слоты и список пропущенных
                response_data = {
                    "created": self.get_serializer(created_slots, many=True).data,
                    "skipped": skipped_slots
                }

                return Response(response_data, status=status.HTTP_201_CREATED)

        else:
            # Одиночная запись
            if not isinstance(times, str):
                return Response({"detail": "Поле 'time' должно быть строкой."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                time = make_aware(datetime.strptime(times, "%Y-%m-%dT%H:%M:%S"))
            except ValueError:
                return Response({"detail": "Неверный формат времени."}, status=status.HTTP_400_BAD_REQUEST)

            if ModeratorSlot.objects.filter(time=time).exists():
                return Response({"detail": "Этот таймслот уже занят."}, status=status.HTTP_400_BAD_REQUEST)

            data['time'] = time
            serializer = self.get_serializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    # Кастомное удаление по времени
    @action(detail=False, methods=['delete'], url_path='delete-bytime', permission_classes=[IsModeratorOrAdmin])
    def delete_by_time(self, request):
        time_str = request.query_params.get('time')
        if not time_str:
            return Response({'detail': 'Параметр `time` обязателен.'}, status=status.HTTP_400_BAD_REQUEST)

        time = parse_datetime(time_str)
        if not time:
            return Response({'detail': 'Неверный формат времени. Используйте ISO 8601 (например, 2025-04-30T15:00:00).'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            music_slot = ModeratorSlot.objects.get(time=time)
        except ModeratorSlot.DoesNotExist:
            return Response({'detail': 'Слот с таким временем не найден.'}, status=status.HTTP_404_NOT_FOUND)

        music_slot.delete()
        return Response({'detail': 'Слот успешно удалён.'}, status=status.HTTP_204_NO_CONTENT)
    

    # Кастомное удаление регулярки
    # @action(detail=False, methods=['delete'], url_path='delete-regular', permission_classes=[IsModeratorOrAdmin])
    # def delete_regular(self, request):
    #     time_str = request.query_params.get('time')  # "15:00"
    #     date_str = request.query_params.get('date')  # "2025-05-03"
    #     moderator_id = request.query_params.get('moderator_id', None)

    #     # 🔒 Проверка параметров
    #     if not time_str or not date_str:
    #         return Response({'detail': 'Параметры `time` и `date` обязательны.'}, status=status.HTTP_400_BAD_REQUEST)

    #     date = parse_date(date_str)
    #     if not date:
    #         return Response({'detail': 'Неверный формат даты. Используйте YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

    #     # 🔐 Проверка прав
    #     if moderator_id:
    #         if not request.user.is_staff and not request.user.is_superuser:
    #             return Response({'detail': 'У вас нет прав удалять чужие слоты.'}, status=status.HTTP_403_FORBIDDEN)
    #     else:
    #         moderator_id = request.user.id

    #     # 🧠 Вычисляем день недели по дате
    #     # date.weekday(): понедельник = 0, воскресенье = 6
    #     # Django ExtractWeekDay: воскресенье = 1, понедельник = 2, ..., суббота = 7
    #     django_weekday = (date.weekday() + 2) % 7 or 7

    #     # 🔍 Фильтруем слоты по дню недели, времени и дате
    #     qs = ModeratorSlot.objects.filter(
    #         moderator_id=moderator_id,
    #         is_regular=True,
    #         time__date__gte=date,
    #         time__time=time_str
    #     ).annotate(
    #         weekday=ExtractWeekDay('time')
    #     ).filter(
    #         weekday=django_weekday
    #     )

    #     deleted_count = qs.count()
    #     qs.delete()

    #     return Response({'detail': f'Удалено {deleted_count} регулярных слотов.'}, status=status.HTTP_200_OK)
