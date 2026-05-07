from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from aportalapi.models import SignupSheet
from aportalapi.serializers import SignupSheetSerializer


class IsSuperUserOrCreateOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method == 'POST':
            return True
        return request.user.is_superuser


class SignupSheetViewSet(viewsets.ModelViewSet):
    queryset = SignupSheet.objects.select_related('user', 'chart').all()
    serializer_class = SignupSheetSerializer
    permission_classes = [IsSuperUserOrCreateOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['delete'], url_path='clear')
    def clear(self, request):
        SignupSheet.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
