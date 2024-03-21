from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, CommentViewSet

router_v1 = DefaultRouter()

router_v1.register(
    r'titles/(?P<titles_id>[^/.]+)/reviews', ReviewViewSet, basename='review')
router_v1.register(
    r'titles/(?P<titles_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments',
    CommentViewSet, basename='comment')
from .views import CategoryViewSet, GenreViewSet, TitleViewSet


router_v1 = DefaultRouter()

router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)


urlpatterns = [
    path('v1/', include(router_v1.urls))
]
