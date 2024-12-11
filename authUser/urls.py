from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from django.conf.urls.static import static
from django.conf import settings
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from drf_spectacular.views import SpectacularSwaggerView


from authUser import views

urlpatterns = [
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='register'),
    # path('register-confirm/<int:pk>/<str:token>/', views.RegisterConfirmView.as_view(), name='register_confirm'),
    path('password-reset/', views.PasswordReset.as_view(), name='password_reset_request'),
    path('password_reset_confirm/<int:pk>/<str:token>/', views.ResetPasswordConfirm.as_view(),
         name='password_reset_confirm'),
    path('current-user/', views.CurrentUserView.as_view(), name='current_user'),
    path('all-users/', views.AllUsersView.as_view(), name='all_users'),
    path('delete-user/<int:pk>/', views.DeleteUser.as_view(), name='delete_user')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)