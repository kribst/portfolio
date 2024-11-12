from django.contrib import admin
from .models import Work, WorkImage, CV, WorkDescription


@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ('id', 'file')
    search_fields = ('file',)


class WorkImageInline(admin.TabularInline):
    model = WorkImage
    extra = 1  # Nombre de formulaires vides à afficher


class WorkDescriptionInline(admin.TabularInline):
    model = WorkDescription
    extra = 1  # Nombre de formulaires vides à afficher


class WorkAdmin(admin.ModelAdmin):
    inlines = [WorkImageInline, WorkDescriptionInline]  # Affiche les images et descriptions associées dans l'interface d'administration
    list_display = ('id', 'name', 'type', 'created_at', 'updated_at', 'link')
    search_fields = ('name', 'type')


admin.site.register(Work, WorkAdmin)