from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from attendance.views import RegisterView

schema_view = get_schema_view(
    openapi.Info(
        title="Attendance Hours API",
        default_version='v1',
        description="Save your attendance hours simple and easy or use https://maschourbank.vercel.app/"
                    " Documentation available in format swagger on /swagger",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="diogobaltazardonascimento@outlook.com.br",
                                url='https://github.com/mascDriver',
                                name='Diogo Baltazar do Nascimento'),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='auth_register'),
    path('attendance/', include('attendance.urls'))
]
