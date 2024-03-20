from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, CommentViewSet

router_v1 = DefaultRouter()

router_v1.register(
    r'titles/(?P<titles_id>[^/.]+)/reviews', ReviewViewSet, basename='review')
router_v1.register(
    r'titles/(?P<titles_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments',
    CommentViewSet, basename='comment')

urlpatterns = [
    path('v1/', include(router_v1.urls))
]
