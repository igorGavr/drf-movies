from django.db import models
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics

from .models import Movie, Actor
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorListSerializer,
    ActorDetailSerializer
)
from .services import get_client_ip


class MovieListView(APIView):
    '''Вивід всіх фільмів'''
    def get(self, request):
        # фільтруємо наш кверісет та додаємо до кожного movie поле rating_user
        movies = Movie.objects.filter(draft=False).annotate(
            # поверне 0 або 1 , в залежності чи ставив юзер рейтинг даному фільму
            rating_user = models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self, request)))
        ).annotate(
            # рахуємо середній рейтинг
            # avg_star = models.Sum(models.F('ratings__star'))/models.Count(models.F('ratings'))
            # avg_star = models.Sum(models.F('ratings__star'))/models.Count('ratings')
            avg_star = (Avg("ratings__star"))
        )
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    '''Вивід фільмa'''
    def get(self, request, pk):
        movie = Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    '''Додавання відгуків'''
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=status.HTTP_201_CREATED)


class AddStarRatingView(APIView):
    """Додавання рейтингу фільму"""
    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ActorsListView(generics.ListAPIView):
    """Вивід всіх акторів та режисерів"""
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    """Вивід всіх акторів та режисерів"""
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer