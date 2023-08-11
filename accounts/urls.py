from django.urls import path

from .views import UserAccountView, accept_reaction, delete_reaction

urlpatterns = [
    path('user/', UserAccountView.as_view(), name='user_accounts'),
    path('accept/<int:pk>', accept_reaction, name='accept'),
    path('delete/<int:pk>', delete_reaction, name='reject'),
]
