from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from aportalapi.models import SignupSheet
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
        SignupSheet.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
