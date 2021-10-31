from django.contrib import admin
from .models import Tarefas, Progressos, Perfis


class TarefasAdmin(admin.ModelAdmin):
    list_display = ('nome',)


admin.site.register(Tarefas, TarefasAdmin)
admin.site.register(Progressos)
admin.site.register(Perfis)
