from rest_framework import viewsets, permissions


from aportalapi.models import Lyrics
from aportalapi.serializers import LyricsSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class LyricsViewSet(viewsets.ModelViewSet):
    queryset = Lyrics.objects.select_related('user').all()
    serializer_class = LyricsSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    http_method_names = ['get', 'post', 'delete']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
