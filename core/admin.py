from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Book, User, History

# Register your models here.
#se customiza la vista del admin (este cambio solo se ve reflejado al acceder)
#al panel admin en django.
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

#se indican los modelos que puede ver el admin desde el panel admin de django.
admin.site.register(Book)
admin.site.register(History)
admin.site.register(User, CustomUserAdmin)

