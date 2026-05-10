from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import Like, Favorite
from .serializers import FavoriteSerializer

from .models import Achievement, Cat

from .serializers import AchievementSerializer, CatSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly] 

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) 
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        cat = self.get_object()
        if cat.owner == request.user:
            return Response(
                {'error': 'Нельзя лайкать своего кота'},
                status=status.HTTP_400_BAD_REQUEST
            )
        like, created = Like.objects.get_or_create(user=request.user, cat=cat)
        if not created:
            like.delete()
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        return Response({'status': 'liked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        cat = self.get_object()
        if cat.owner == request.user:
            return Response(
                {'error': 'Нельзя добавлять в избранное своего кота'},
                status=status.HTTP_400_BAD_REQUEST
            )
        favorite, created = Favorite.objects.get_or_create(user=request.user, cat=cat)
        if not created:
            favorite.delete()
            return Response({'status': 'removed from favorites'}, status=status.HTTP_200_OK)
        return Response({'status': 'added to favorites'}, status=status.HTTP_200_OK)
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def likes_count(self, request, pk=None):
        cat = self.get_object()
        count = cat.likes.count()
        return Response({'likes_count': count}, status=status.HTTP_200_OK)
class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    pagination_class = None

class FavoriteListView(generics.ListAPIView):
    serializer_class = CatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cat.objects.filter(favorited_by__user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class LikeListView(generics.ListAPIView):
    serializer_class = CatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cat.objects.filter(likes__user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)