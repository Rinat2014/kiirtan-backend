# moderators/filters.py

import django_filters
from .models import ModeratorSlot

class ModeratorSlotFilter(django_filters.FilterSet):
    from_date = django_filters.DateTimeFilter(field_name="time", lookup_expr='gte')
    to_date = django_filters.DateTimeFilter(field_name="time", lookup_expr='lte')
    time = django_filters.IsoDateTimeFilter(field_name="time") 

    class Meta:
        model = ModeratorSlot
        fields = ['id', 'from_date', 'to_date', 'time', 'moderator', 'is_regular']


# http://localhost:8000/api/music-slots/?from_date=2025-04-30T00:00:00&to_date=2025-05-05T23:59:59
# http://localhost:8000/api/music-slots/?from_date=2025-04-01T00:00:00&to_date=2025-04-30T23:59:59

# http://localhost:8000/api/music-slots/?from_date=2025-04-01T00:00:00&to_date=2025-04-30T23:59:59&musician=5&is_regular=true&musician=5&is_regular=true

# http://localhost:8000/api/music-slots/?time=2025-04-28T19:00:00