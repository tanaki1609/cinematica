from django.urls import path
from . import views
from .constants import LIST_CREATE, RETRIEVE_UPDATE_DESTROY

urlpatterns = [
    path('', views.FilmListCreateAPIView.as_view()),
    path('<int:id>/', views.film_detail_api_view),
    path('genres/', views.GenreListAPIView.as_view()),
    path('genres/<int:id>/', views.GenreDetailAPIView.as_view()),
    path('directors/', views.DirectorViewSet.as_view(LIST_CREATE)),
    path('directors/<int:id>/', views.DirectorViewSet.as_view(RETRIEVE_UPDATE_DESTROY))
]
