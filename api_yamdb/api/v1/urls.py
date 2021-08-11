from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, ReviewViewSet, UserViewSet, send_confirmation_code

router_v1 = DefaultRouter(trailing_slash='optional')
router_v1.register('users/?', UserViewSet)
router_v1.register(
    r'titles/(?P<titles_id>\d+)/reviews/?',
    ReviewViewSet, basename="reviews")
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/?',
    CommentViewSet, basename="comments")


urlpatterns = [
    path('auth/signup/', send_confirmation_code, name='send_code'),
    # path('auth/token', ...),
    path('', include(router_v1.urls)),    
]
