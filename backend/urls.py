from django.contrib import admin
from django.urls import include, path

from . import settings
from core.views import add_student
from core.views import get_students_preferences


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path("admin/", admin.site.urls),
    path('add-student/', add_student, name='add_student'),
    path('get-prefs/', get_students_preferences, name='get_prefs'),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include("debug_toolbar.urls")),
    ] + urlpatterns
