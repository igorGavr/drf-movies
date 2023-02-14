from django.db import models
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics, permissions

from .models import Movie, Actor
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorListSerializer,
    ActorDetailSerializer
)
from .services import get_client_ip, MovieFilter, PaginationMovies
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    '''Вивід всіх фільмів'''
    filterset_class = MovieFilter
    pagination_class = PaginationMovies



    def get_queryset(self):
        # фільтруємо наш кверісет та додаємо до кожного movie поле rating_user
        movies = Movie.objects.filter(draft=False).annotate(
            # поверне 0 або 1 , в залежності чи ставив юзер рейтинг даному фільму
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            # рахуємо середній рейтинг
            # avg_star = models.Sum(models.F('ratings__star'))/models.Count(models.F('ratings'))
            # avg_star = models.Sum(models.F('ratings__star'))/models.Count('ratings')
            avg_star=(Avg("ratings__star"))
        )
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == 'retrieve':
            return MovieDetailSerializer


class MovieListView(generics.ListAPIView):
    '''Вивід всіх фільмів'''
    serializer_class = MovieListSerializer
    # якщо додали фільтри в настройки то цю стрічку можна не писати
    # filter_backends = (DjangoFilterBackend, )
    filterset_class = MovieFilter
    permission_classes = [permissions.IsAuthenticated]
    # це на випадок якщо нам потрібна проста фільтрація на основі рівності
    # filterset_fields = ['title', 'country']
    # ми також можемо виконувати звязаний пошук по полю FK або M2M
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['category__name']

    def get_queryset(self):
        # фільтруємо наш кверісет та додаємо до кожного movie поле rating_user
        movies = Movie.objects.filter(draft=False).annotate(
            # поверне 0 або 1 , в залежності чи ставив юзер рейтинг даному фільму
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            # рахуємо середній рейтинг
            # avg_star = models.Sum(models.F('ratings__star'))/models.Count(models.F('ratings'))
            # avg_star = models.Sum(models.F('ratings__star'))/models.Count('ratings')
            avg_star=(Avg("ratings__star"))
        )
        return movies


# class MovieListView(APIView):
#     '''Вивід всіх фільмів'''
#
#     def get(self, request):
#         # фільтруємо наш кверісет та додаємо до кожного movie поле rating_user
#         movies = Movie.objects.filter(draft=False).annotate(
#             # поверне 0 або 1 , в залежності чи ставив юзер рейтинг даному фільму
#             rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self, request)))
#         ).annotate(
#             # рахуємо середній рейтинг
#             # avg_star = models.Sum(models.F('ratings__star'))/models.Count(models.F('ratings'))
#             # avg_star = models.Sum(models.F('ratings__star'))/models.Count('ratings')
#             avg_star=(Avg("ratings__star"))
#         )
#         serializer = MovieListSerializer(movies, many=True)
#         return Response(serializer.data)


class MovieDetailView(generics.RetrieveAPIView):
    '''Вивід фільмa'''
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


# class MovieDetailView(APIView):
#     '''Вивід фільмa'''
#     def get(self, request, pk):
#         movie = Movie.objects.get(id=pk, draft=False)
#         serializer = MovieDetailSerializer(movie)
#         return Response(serializer.data)


# CRUD+LIST
class ReviewCreateViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewCreateSerializer


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer


# class ReviewCreateView(APIView):
#     '''Додавання відгуків'''
#
#     def post(self, request):
#         review = ReviewCreateSerializer(data=request.data)
#         if review.is_valid():
#             review.save()
#         return Response(status=status.HTTP_201_CREATED)


class AddStarRatingViewSet(viewsets.ModelViewSet):
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip = get_client_ip(self.request))



class AddStarRatingView(generics.CreateAPIView):
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip = get_client_ip(self.request))


# class AddStarRatingView(APIView):
#     """Додавання рейтингу фільму"""
#
#     def post(self, request):
#         serializer = CreateRatingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(ip=get_client_ip(request))
#             return Response(status=status.HTTP_201_CREATED)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)


class ActorsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вивід всіх акторів та режисерів"""
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializer
        elif self.action == 'retrieve':
            return ActorDetailSerializer


class ActorsListView(generics.ListAPIView):
    """Вивід всіх акторів та режисерів"""
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']



class ActorDetailView(generics.RetrieveAPIView):
    """Вивід всіх акторів та режисерів"""
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
