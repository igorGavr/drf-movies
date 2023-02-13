from rest_framework import serializers
from .models import Movie, Review, Rating, Actor


class FilterReviewListSerializer(serializers.ListSerializer):
    """Вивід тільки батьківських коментів"""

    def to_representation(self, data):
        # фільтруємо кверісет
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """ Рекурсивний вивід дочірніх відгуків"""

    # value - це значення одного запису з бази даних
    # в даному методі ми шукаємо всіх наших дітей
    # які завязані на нашому відгуку
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ActorListSerializer(serializers.ModelSerializer):
    """Вивід списку акторів та режисерів"""

    class Meta:
        model = Actor
        fields = ("id", "name", "image")


class ActorDetailSerializer(serializers.ModelSerializer):
    """Вивід повного опису актора або режисера"""

    class Meta:
        model = Actor
        fields = "__all__"


class MovieListSerializer(serializers.ModelSerializer):
    """Список фільмів"""
    rating_user = serializers.BooleanField()
    # avg_star = serializers.DecimalField(max_digits=2, decimal_places=1)
    avg_star = serializers.FloatField()

    class Meta:
        model = Movie
        fields = ("id", "title", "tagline", "category", "rating_user", "avg_star")


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    # для того щоб наш звязок працював, ми додали
    # в class Review(models.Model) в поле parent - related_name='children'
    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ("name", "text", "children", "id")


class MovieDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = ActorDetailSerializer(read_only=True, many=True)
    actors = ActorListSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    # для того щоб ми змогли бачити відгуки, ми додали
    # в class Review(models.Model) в поле movie - related_name='reviews'
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ("draft",)


class CreateRatingSerializer(serializers.ModelSerializer):
    """Додавання рейтингу користувачем"""

    class Meta:
        model = Rating
        fields = ('star', 'movie')

    def create(self, validated_data):

        rating, created = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get('star')}
        )
        return rating
