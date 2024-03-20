from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, CommentViewSet, TitleViewSet

router_v1 = DefaultRouter()

router_v1.register('titles', TitleViewSet, basename='title')
router_v1.register(
    r'titles/(?P<titles_id>\d+)/reviews', ReviewViewSet, basename='review')
router_v1.register(
    r'titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment')

urlpatterns = [
    path('v1/', include(router_v1.urls))
]
