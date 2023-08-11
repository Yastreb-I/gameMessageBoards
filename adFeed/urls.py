from django.urls import path
# импортируем наше представление
from .views import Advertisements, AdsDetailView, AdCreateView, AdUpdateView, AdDeleteView


urlpatterns = [
    path('', Advertisements.as_view(), name="ad_feed"),
    path('<int:pk>', AdsDetailView.as_view(), name="ad_blog"),
    path('add', AdCreateView.as_view(), name='ad_create'),  # Ссылка на создание статьи
    path('update/<int:pk>', AdUpdateView.as_view(), name="ad_update"),  # Ссылка на редактирование статьи
    path('delete/<int:pk>', AdDeleteView.as_view(), name="ad_delete"),  # Ссылка на удаление статьи

]

