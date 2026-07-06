import uuid

from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from aportalapi.models import Chart, Lyrics, SignupSheet
from aportalapi.serializers import SignupSheetSerializer


class IsSuperUserOrCreateOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in ('POST', 'PATCH', 'GET'):
            return True
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method in ('GET', 'PATCH'):
            return obj.user == request.user
        return False


class SignupSheetViewSet(viewsets.ModelViewSet):
    serializer_class = SignupSheetSerializer
    permission_classes = [IsSuperUserOrCreateOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        qs = SignupSheet.objects.select_related('user', 'user__user_utilities', 'chart', 'lyrics')
        if self.request.user.is_superuser:
            return qs.all()
        return qs.filter(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='mine')
    def mine(self, request):
        try:
            signup = SignupSheet.objects.select_related('user', 'chart').get(user=request.user)
            return Response(SignupSheetSerializer(signup).data)
        except SignupSheet.DoesNotExist:
            return Response({'detail': 'Not signed up.'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        existing = SignupSheet.objects.filter(user=request.user).first()
        if existing:
            return Response(SignupSheetSerializer(existing).data, status=status.HTTP_200_OK)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['delete'], url_path='clear')
    def clear(self, request):
        User.objects.filter(username__startswith='guest_').delete()
        SignupSheet.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GuestSignupView(APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        first_name = request.data.get('first_name', '').strip()
        last_name = request.data.get('last_name', '').strip()
        if not first_name:
            return Response({'first_name': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        username = f'guest_{uuid.uuid4().hex[:12]}'
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name)

        try:
            chart = None
            chart_file = request.FILES.get('chart_file')
            if chart_file:
                chart = Chart.objects.create(user=user, chart_file=chart_file)

            lyrics = None
            lyrics_file = request.FILES.get('lyrics_file')
            if lyrics_file:
                lyrics = Lyrics.objects.create(user=user, lyrics_file=lyrics_file)

            signup = SignupSheet.objects.create(user=user, chart=chart, lyrics=lyrics)
        except Exception:
            user.delete()
            return Response({'detail': 'Failed to process upload.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SignupSheetSerializer(signup, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
