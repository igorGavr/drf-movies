from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = format_suffix_patterns([
    path('movies/', views.MovieViewSet.as_view({'get':'list'})),
    path('movies/<int:pk>/', views.MovieViewSet.as_view({'get':'retrieve'})),

    path('review/', views.ReviewCreateViewSet.as_view({'post':'create'})),
    path('rating/', views.AddStarRatingViewSet.as_view({'post':'create'})),

    path('actors/', views.ActorsViewSet.as_view({'get':'list'})),
    path('actors/<int:pk>/', views.ActorsViewSet.as_view({'get':'retrieve'})),
])

# urlpatterns = [
#     path('movies/', views.MovieListView.as_view()),
#     path('movies/<int:pk>/', views.MovieDetailView.as_view()),
#     path('review/', views.ReviewCreateView.as_view()),
#     path('rating/', views.AddStarRatingView.as_view()),
#     path('actors/', views.ActorsListView.as_view()),
#     path('actors/<int:pk>/', views.ActorDetailView.as_view()),
# ]