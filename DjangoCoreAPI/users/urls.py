from django.urls import path
from users.views import RegisterView, LoginView, RetrieveUserView, UpdateUserView, ChangePasswordUserView, DeleteUserView, GetUserByIdView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('retrieve/', RetrieveUserView.as_view(), name='user_detail'),
    path('update/', UpdateUserView.as_view(), name='user_update'),
    path('change-password/', ChangePasswordUserView.as_view(), name='change_password'),
    path('delete/', DeleteUserView.as_view(), name='user_delete'),
    path('user/<int:pk>', GetUserByIdView.as_view(), name="get-user-by-id")
]