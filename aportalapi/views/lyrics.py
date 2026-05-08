from rest_framework import viewsets, permissions

from aportalapi.models import Lyrics
from aportalapi.serializers import LyricsSerializer


class IsChartOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            chart = view.get_chart_from_request()
            return chart is not None and chart.user == request.user
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.chart.user == request.user


class LyricsViewSet(viewsets.ModelViewSet):
    queryset = Lyrics.objects.select_related('chart').all()
    serializer_class = LyricsSerializer
    permission_classes = [IsChartOwnerOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_chart_from_request(self):
        from aportalapi.models import Chart
        try:
            chart_id = self.request.data.get('chart')
            return Chart.objects.get(pk=chart_id)
        except (Chart.DoesNotExist, TypeError, ValueError):
            return None
