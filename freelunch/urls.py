from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from organization.views import InvitationViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = DefaultRouter()
router.register(r'invitations', InvitationViewSet)

# Schema view for DRF-YASG
schema_view = get_schema_view(
    openapi.Info(
        title="Free Lunch API",
        default_version="v1",
        description="An API to handle the backend of free-lunch application",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('users/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/', include('lunches.urls')),
    path('api/', include('users.urls')),
    path('api/', include('withdrawals.urls')),
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
]

