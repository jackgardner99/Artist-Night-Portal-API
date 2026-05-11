from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from aportalapi.models import Chart
from aportalapi.serializers import ChartSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class ChartViewSet(viewsets.ModelViewSet):
    queryset = Chart.objects.select_related('user').all()
    serializer_class = ChartSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    http_method_names = ['get', 'post', 'delete']

    def create(self, request, *args, **kwargs):
        file = request.FILES.get('chart_file')
        if file:
            existing = Chart.objects.filter(
                user=request.user,
                chart_file__endswith=file.name
            ).first()
            if existing:
                return Response(ChartSerializer(existing).data, status=status.HTTP_200_OK)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
