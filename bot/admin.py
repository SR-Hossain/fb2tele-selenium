from django.contrib import admin

from bot.models import Post


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id','sender', 'permalink', 'content', 'summary')
    ordering = ('-id',)