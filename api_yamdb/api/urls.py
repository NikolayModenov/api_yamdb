from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import SignUpView

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
]
