from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import ProductManager, Project, Student, Team, User, Week
from .models import TimeSlot
from .models import StudentProjectPreferences


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = (
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )

    fieldsets = (
        (None, {"fields": ("email", "name", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


class TimeSlotInline(admin.TabularInline):
    model = TimeSlot
    extra = 1
    fields = ['start', 'end']


@admin.register(ProductManager)
class ProductManagerAdmin(admin.ModelAdmin):
    inlines = [
        TimeSlotInline
    ]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    inlines = [
        TimeSlotInline
    ]


admin.site.register(Project)
admin.site.register(Team)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Week)
admin.site.register(TimeSlot)
admin.site.register(StudentProjectPreferences)
