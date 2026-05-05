# backend/users/admin.py
from django.contrib import admin
from .models import User, UserLink

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'email', 'username', 'utc_offset', 'is_active', 'is_musician', 'is_moderator_musicians', 'is_editor', 'is_admin', 'is_moderator_site')
#     list_filter = ('is_active', 'is_musician', 'is_moderator_musicians', 'is_editor', 'is_admin', 'is_moderator_site')


# @admin.register(LinkType)
# class LinkTypeAdmin(admin.ModelAdmin):
#     list_display = ("id", "name", "display_name", "icon")
#     search_fields = ("name", "display_name")



# # class UserLinkInline(admin.TabularInline):
# #     model = UserLink
# #     extra = 1


# @admin.register(UserLink)
# class UserLinkAdmin(admin.ModelAdmin):
#     list_display = ("id", "user", "link_type", "url")
#     # search_fields = ("name", "display_name")



class UserLinkInline(admin.TabularInline):  # или admin.StackedInline для вертикального расположения
    model = UserLink
    extra = 1  # количество пустых форм для добавления новых ссылок
    fields = ['name', 'url']
    # autocomplete_fields = ['userlink']  # удобный поиск по ссылкам




@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "utc_offset",
        "is_active",
        "is_staff",
        "get_groups",
        "last_login",
        "date_joined",
    )
    list_filter = ("is_active", "groups")  # фильтровать по группам удобно
    inlines = [UserLinkInline]  # добавил inline для ссылок


    def get_groups(self, obj):
        """Выводим список групп пользователя через запятую"""
        return ", ".join([g.name for g in obj.groups.all()])

    get_groups.short_description = "Groups"


    def get_links_count(self, obj):
        """Выводим количество ссылок пользователя"""
        return obj.links.count()
    get_links_count.short_description = "Links Count"





@admin.register(UserLink)
class UserLinkAdmin(admin.ModelAdmin):
    list_display = ("get_username", "name", "url", "public")
    list_filter = ("user__username",)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'User Name'
    get_username.admin_order_field = 'user__username'

# @admin.register(UserLink)
# class UserLinkAdmin(admin.ModelAdmin):
#     list_display = ( "user.username", "name", "url")
#     search_fields = ("user", "name", "url")

    
    # def get_users_count(self, obj):
    #     """Выводим количество пользователей с этой ссылкой"""
    #     return obj.user.count()
    # get_users_count.short_description = "Users Count"