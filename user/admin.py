from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


# 为Profile创建一个数据行
class ProfileInline(admin.StackedInline):
    # 模型是Profile
    model = Profile
    can_delete = False

# 重新设计了User模型在admin上的显示
class UserAdmin(BaseUserAdmin):
    # 为了在admin界面显示Profile的字段，定义inlines为上面的类
    inlines = (ProfileInline, )
    list_display = ('username', 'nickname', 'email', 'is_staff', 'is_active', 'is_superuser')

    def nickname(self, obj):
        return obj.profile.nickname
    nickname.short_description = '昵称'

# Re-register UserAdmin
admin.site.unregister(User)
# 因为重新设计了UserAdmin，所以要重新register
admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname')