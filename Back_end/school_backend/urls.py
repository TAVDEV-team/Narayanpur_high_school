from django.contrib import admin
from django.urls import path,include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(
        [
            path('nphs/', include('nphs_school.urls')),
            path('funds/', include('fund.urls')),
            path('user/',include('accounts.urls')),
        ]
    )),
    # 📄 API Schema + Swagger Docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema')),
]
