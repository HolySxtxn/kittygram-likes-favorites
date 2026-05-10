from rest_framework import routers
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from cats.views import AchievementViewSet, CatViewSet, FavoriteListView, LikeListView, FavoriteViewSet

router = routers.DefaultRouter()
router.register(r'cats', CatViewSet)
router.register(r'achievements', AchievementViewSet)
router.register(r'favorites-detail', FavoriteViewSet, basename='favorite-detail')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('djoser.urls')),  
    path('api/', include('djoser.urls.authtoken')), 
    
    path('api/favorites/', FavoriteListView.as_view(), name='favorites'),
    path('api/my-likes/', LikeListView.as_view(), name='my-likes'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    