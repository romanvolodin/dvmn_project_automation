from django.urls import path
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect

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


class ProjectAdmin(admin.ModelAdmin):
    change_list_template = "admin/project_change_list.html"

    def get_urls(self):
        urls = super(ProjectAdmin, self).get_urls()
        custom_urls = [
            path(
                "distribute_students/",
                self.distribute_students,
                name="distribute_students",
            ),
            path(
                "send_notifications/",
                self.send_notifications,
                name="send_notifications",
            ),
        ]
        return custom_urls + urls

    def distribute_students(self, request):
        self.message_user(request, "Студенты распределены")
        return HttpResponseRedirect("../")

    def send_notifications(self, request):
        self.message_user(request, "Уведомления разосланы")
        return HttpResponseRedirect("../")


admin.site.register(ProductManager)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Student)
admin.site.register(Team)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Week)
admin.site.register(TimeSlot)
admin.site.register(StudentProjectPreferences)
