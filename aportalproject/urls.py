from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from aportalapi.views.profile import MyProfileView, UserProfileView
from aportalapi.views.charts import ChartViewSet
from aportalapi.views.signup_sheet import SignupSheetViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'charts', ChartViewSet, basename='chart')
router.register(r'signup-sheet', SignupSheetViewSet, basename='signup-sheet')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/me', MyProfileView.as_view(), name='my-profile'),
    path('profile/<int:pk>', UserProfileView.as_view(), name='user-profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
