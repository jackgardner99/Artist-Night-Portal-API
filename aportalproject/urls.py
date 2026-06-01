from django.urls import include, path
from rest_framework import routers
from aportalapi.views.auth import RegisterView, LoginView
from aportalapi.views.profiles import MyProfileView, UserProfileView, UserProfileListView
from aportalapi.views.charts import ChartViewSet
from aportalapi.views.signup_sheet import SignupSheetViewSet
from aportalapi.views.lyrics import LyricsViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'charts', ChartViewSet, basename='chart')
router.register(r'signup-sheet', SignupSheetViewSet, basename='signup-sheet')
router.register(r'lyrics', LyricsViewSet, basename='lyrics')

urlpatterns = [
    path('', include(router.urls)),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('profiles', UserProfileListView.as_view(), name='profile-list'),
    path('profiles/me', MyProfileView.as_view(), name='my-profile'),
    path('profiles/<int:pk>', UserProfileView.as_view(), name='user-profile'),
]
