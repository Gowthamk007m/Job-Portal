from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls", namespace="core")),
    path("job/", include("jobs.urls", namespace="job")),
    path("job-profile/", include("job_profile.urls", namespace="job_profile")),
    path("accounts/", include("user.urls", namespace="user")),
    path("administrator/", include("admin_panel.urls", namespace="admin-d")),
    path('tinymce/', include('tinymce.urls')),
    path("select2/", include("django_select2.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
