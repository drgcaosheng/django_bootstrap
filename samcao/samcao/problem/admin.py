from django.contrib import admin
from samcao.problem.models import System,User,Type,Way


class TypeAdmin(admin.ModelAdmin):
    list_display=('way_type','system_name')

class UserAdmin(admin.ModelAdmin):
    list_display=('user_name','pass_word')

class WayAdmin(admin.ModelAdmin):
    list_display=('Key_world','Key_world','user_name','system_name','way_type','way','ban_fa')
    search_fields = ('Key_world','ban_fa')
    # list_filter=('user_name')

admin.site.register(System)
admin.site.register(User,UserAdmin)
admin.site.register(Type,TypeAdmin)
admin.site.register(Way,WayAdmin)
