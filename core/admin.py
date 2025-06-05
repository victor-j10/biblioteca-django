from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Book, User, History

# Register your models here.
class CustomUserAdmin(BaseUserAdmin):
    model = User

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': ('name', 'role', 'borrowed_books'),
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Información adicional', {
            'fields': ('name', 'role'),
        }),
    )

    filter_horizontal = ('borrowed_books',)

admin.site.register(Book)
admin.site.register(History)
admin.site.register(User, CustomUserAdmin)

