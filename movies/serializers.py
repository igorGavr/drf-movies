from rest_framework import serializers
from .models import Movie, Review, Rating


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


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("title", "tagline", "category",)


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
    directors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
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
        fields = ("star", "movie")

    def create(self, validated_data):
        rating = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star':validated_data.get('star')}
        )
        return rating