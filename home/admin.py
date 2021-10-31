from django.contrib import admin
from .models import Coisa,Grupo,GrupoCell


class CoisaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'cont', 'dono', 'tag', 'grupo', 'data')
    list_filter = ('titulo', 'dono', 'tag', 'grupo', 'data')
    list_editable = ('tag',)


admin.site.register(Coisa, CoisaAdmin)
admin.site.register(Grupo)
admin.site.register(GrupoCell)

# Register your models here.
