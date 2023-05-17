from django.contrib import admin
from django.urls import path, include
from . import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # path('', views.index, name='index'),
    path('profiles/', views.profile_list),
    path('profile/<str:userID>/', views.profile_detail),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('getProfile/', views.getProfile),
    path('updateProfile/', views.updateProfile),
    path('updateProfilePicture/', views.updateProfilePicture),
    path('updateCoverPage/', views.updateCoverPage),
    path('initialize/<str:userID>/',views.initializeProfile),
    path('signup/',views.signup),
    path('getField/',views.getExtraField),
    path('fieldUpdate/',views.updateFields),
    path('sendVerificationCode/',views.sendVerificationMail),
    path('verifyEmail/',views.verifyEmail),
     path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]